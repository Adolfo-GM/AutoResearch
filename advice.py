import random

advice = [
    "Try something radically different. Go for a completely different architecture.",
    "Try creating new mechanisms that are more efficient than attention.",
    "If progress stalls, change the inductive bias instead of tuning hyperparameters.",
    "Try sparsity. Dense computation may be wasting capacity.",
    "Experiment with parameter sharing or weight tying.",
    "Try branching computation instead of purely sequential layers.",
    "Consider whether depth or width is the real bottleneck.",
    "Try adding recurrence or memory instead of more layers.",
    "Test whether a smaller model trains better before scaling up.",
    "Try a mixture-of-experts style routing mechanism.",
    "If training is unstable, simplify the architecture.",
    "Try replacing components rather than stacking more of them.",
    "Look for unnecessary computation and remove it.",
    "Try introducing stochasticity into the architecture.",
    "If results plateau, redesign the computational graph entirely.",
    "Improve algorithmic speed. If model trains faster, it will be able to train for more epochs in the time limit.",
    "Make the architecture more compute efficient. If we can do more with less, we can train for longer. O(n^2) -> O(n log n) or O(n) and then even O(log n) or O(1).",
    
]

def get_advice():
    return random.choice(advice)

if __name__ == "__main__":
    print(get_advice())