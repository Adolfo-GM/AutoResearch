
# AutoResearch Lab

An experimental sandbox for autonomous AI research and development. This repository provides a structured environment for iterative training, version control, and performance benchmarking of character-level language models.

![Benchmark Chart](logger_research/benchmark_chart.png)

## Overview
The AutoResearch Lab is designed to enable AI agents to perform independent experiments. It features a custom micro-gradient engine, automated version control, and real-time logging to track progress and validate research hypotheses.

## Project Components
- `train.py`: Core research script containing the model architecture and training loop.
- `saver.py`: Automated versioning utility for archiving and restoring experiment states.
- `logger.py`: Centralized telemetry for recording loss metrics and metadata.
- `benchmark.py`: Analytics suite for ranking experiments and generating performance visualizations.

## Operational Commands

### Version Control
```bash
# Backup current research state
python saver.py <filename>

# Restore a specific version
python saver.py --restore Saver_Branches/<timestamped_file>
```

### Research Logging
```bash
python3 logger.py --research_name "id" --filename_in_saver "path/to/backup" --loss "#.###"
```

### Analytics
```bash
# View ranked results and update benchmark_chart.png
python benchmark.py
```

## Research Workflow
1. **Preserve**: Backup `train.py` before any modifications.
2. **Iterate**: Modify `train.py` to test new hypotheses.
3. **Execute**: Run training with a strict **60-second time limit**.
4. **Archive**: Save the resulting version of `train.py`.
5. **Log**: Record metrics in the research database.
6. **Analyze**: Run `benchmark.py` every 10 iterations to evaluate progress.

## Mandatory Rules
- **Target Selection**: Only `train.py` is authorized for modification by the AI agent.
- **Dependency Control**: Use only standard Python libraries (e.g., `math`, `random`).
- **Timing**: Training runs must NOT exceed 60 seconds.
- **Frontier**: You cannot decrease the context length of the model, you may increase it. It can never be smaller than the initial run which is `block_size = 16`.