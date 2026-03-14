import os
import math
import random
import time
random.seed(2026)

docs = [line.strip() for line in open('data.txt') if line.strip()]
random.shuffle(docs)
print(f"num docs: {len(docs)}")

uchars = sorted(set(''.join(docs)))
BOS = len(uchars)
vocab_size = len(uchars) + 1
print(f"vocab size: {vocab_size}")

class Value:
    __slots__ = ('data', 'grad', '_children', '_local_grads')

    def __init__(self, data, children=(), local_grads=()):
        self.data = data
        self.grad = 0
        self._children = children
        self._local_grads = local_grads

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data + other.data, (self, other), (1, 1))

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data * other.data, (self, other), (other.data, self.data))

    def __pow__(self, other): return Value(self.data**other, (self,), (other * self.data**(other-1),))
    def log(self): return Value(math.log(max(1e-15, self.data)), (self,), (1/max(1e-15, self.data),))
    def exp(self):
        clipped = max(-20, min(20, self.data))
        return Value(math.exp(clipped), (self,), (math.exp(clipped),))
    def relu(self): return Value(max(0, self.data), (self,), (float(self.data > 0),))
    def __neg__(self): return self * -1
    def __radd__(self, other): return self + other
    def __sub__(self, other): return self + (-other)
    def __rsub__(self, other): return other + (-self)
    def __rmul__(self, other): return self * other
    def __truediv__(self, other): return self * other**-1
    def __rtruediv__(self, other): return other * self**-1

    def backward(self):
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._children:
                    build_topo(child)
                topo.append(v)
        build_topo(self)
        self.grad = 1
        for v in reversed(topo):
            for child, local_grad in zip(v._children, v._local_grads):
                child.grad += local_grad * v.grad

n_layer = 2
n_embd = 10
block_size = 24
n_head = 1
head_dim = n_embd // n_head
matrix = lambda nout, nin, std=0.08: [[Value(random.gauss(0, std)) for _ in range(nin)] for _ in range(nout)]

# State Dict with Weight Tying
state_dict = {
    'wte': matrix(vocab_size, n_embd), 
    'wpe': matrix(block_size, n_embd)
}
state_dict['lm_head'] = state_dict['wte'] # Weight Tying

for i in range(n_layer):
    state_dict[f'layer{i}.attn_wq'] = matrix(n_embd, n_embd)
    state_dict[f'layer{i}.attn_wk'] = matrix(n_embd, n_embd)
    state_dict[f'layer{i}.attn_wv'] = matrix(n_embd, n_embd)
    state_dict[f'layer{i}.attn_wo'] = matrix(n_embd, n_embd)
    state_dict[f'layer{i}.mlp_fc1'] = matrix(3 * n_embd, n_embd)
    state_dict[f'layer{i}.mlp_fc2'] = matrix(n_embd, 3 * n_embd)
    # Input-dependent decay
    state_dict[f'layer{i}.decay_w'] = matrix(1, n_embd)
    state_dict[f'layer{i}.decay_b'] = [Value(2.5)]
    # SkipInit learnable scales
    state_dict[f'layer{i}.attn_alpha'] = [Value(0.05)]
    state_dict[f'layer{i}.mlp_alpha'] = [Value(0.05)]
params = [p for mat in state_dict.values() for row in (mat if isinstance(mat[0], list) else [mat]) for p in row]
params = list(dict.fromkeys(params))
print(f"num params: {len(params)}")

def linear(x, w):
    return [sum(wi * xi for wi, xi in zip(wo, x)) for wo in w]

def softmax(logits):
    max_val = max(val.data for val in logits)
    exps = [(val - max_val).exp() for val in logits]
    total = sum(exps)
    return [e / total for e in exps]

def rmsnorm(x):
    ms = sum(xi * xi for xi in x) / len(x)
    scale = (ms + 1e-5) ** -0.5
    return [xi * scale for xi in x]

def gpt(token_id, pos_id, kv_state):
    tok_emb = state_dict['wte'][token_id]
    pos_emb = state_dict['wpe'][pos_id]
    x = [t + p for t, p in zip(tok_emb, pos_emb)]
    x = rmsnorm(x)

    for li in range(n_layer):
        x_norm = rmsnorm(x)
        
        # Parallel Linear Attention
        q = linear(x_norm, state_dict[f'layer{li}.attn_wq'])
        k = linear(x_norm, state_dict[f'layer{li}.attn_wk'])
        v = linear(x_norm, state_dict[f'layer{li}.attn_wv'])
        
        d_logit = linear(x_norm, state_dict[f'layer{li}.decay_w'])[0] + state_dict[f'layer{li}.decay_b'][0]
        gate = 1 / (1 + (-d_logit).exp())
        
        for j in range(n_embd):
            kv_state[li][j] = gate * kv_state[li][j] + k[j] * v[j]
        
        attn_out = [q[j] * kv_state[li][j] for j in range(n_embd)]
        attn_out = linear(attn_out, state_dict[f'layer{li}.attn_wo'])
        
        # Parallel MLP with GeLU approximation
        mlp_out = linear(x_norm, state_dict[f'layer{li}.mlp_fc1'])
        # GeLU(x) ~ x * sigmoid(1.702 * x)
        mlp_out = [val / (1 + (-1.702 * val).exp()) for val in mlp_out]
        mlp_out = linear(mlp_out, state_dict[f'layer{li}.mlp_fc2'])
        
        # SkipInit residuals
        aa = state_dict[f'layer{li}.attn_alpha'][0]
        am = state_dict[f'layer{li}.mlp_alpha'][0]
        x = [xi + aa * ai + am * mi for xi, ai, mi in zip(x, attn_out, mlp_out)]

    logits = linear(x, state_dict['lm_head'])
    return logits

learning_rate, beta1, beta2, eps_adam = 0.038, 0.9, 0.999, 1e-8
m = [0.0] * len(params)
v = [0.0] * len(params)

start_time = time.time()
target_duration = 58
step = 0

while True:
    elapsed = time.time() - start_time
    if elapsed >= target_duration:
        break

    doc = docs[step % len(docs)]
    tokens = [BOS] + [uchars.index(ch) for ch in doc] + [BOS]
    n = min(block_size, len(tokens) - 1)

    kv_state = [[Value(0.0) for _ in range(n_embd)] for _ in range(n_layer)]
    losses = []
    for pos_id in range(n):
        token_id, target_id = tokens[pos_id], tokens[pos_id + 1]
        logits = gpt(token_id, pos_id, kv_state)
        probs = softmax(logits)
        loss_t = -probs[target_id].log()
        losses.append(loss_t)
    loss = (1 / n) * sum(losses)

    loss.backward()

    lr_t = learning_rate * max(0.0, 1 - elapsed / target_duration)
    for i, p in enumerate(params):
        m[i] = beta1 * m[i] + (1 - beta1) * p.grad
        v[i] = beta2 * v[i] + (1 - beta2) * p.grad ** 2
        m_hat = m[i] / (1 - beta1 ** (step + 1))
        v_hat = v[i] / (1 - beta2 ** (step + 1))
        p.data -= lr_t * m_hat / (v_hat ** 0.5 + eps_adam)
        p.grad = 0

    print(f"step {step+1:4d} | elapsed {elapsed:.1f}s / {target_duration}s | loss {loss.data:.4f}", end='\r')
    step += 1

print(f"\nfinal_loss={loss.data:.4f}")

temperature = 0.5
print("\n--- inference ---")
for sample_idx in range(20):
    kv_state = [[Value(0.0) for _ in range(n_embd)] for _ in range(n_layer)]
    token_id = BOS
    sample = []
    for pos_id in range(block_size):
        logits = gpt(token_id, pos_id, kv_state)
        probs = softmax([l / temperature for l in logits])
        token_id = random.choices(range(vocab_size), weights=[p.data for p in probs])[0]
        if token_id == BOS:
            break
        sample.append(uchars[token_id])
    print(f"sample {sample_idx+1:2d}: {''.join(sample)}")
