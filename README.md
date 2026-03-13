# AutoResearch

This project is intended to be a lab that allows an AI agent to run AI experiments and the validation suite allows the research to be tested and validated, all research is organized, versioned and validated. This lab allows AI to perform independent artificial intelligence research and development.

### File Backups
You can use the `saver.py` script to back up a file by running `python saver.py <filename>`. It uses a `Saver` class to automatically create a `Saver_Branches/` directory, saving a copy of the specified file with the current date and time down to the second in the format `filename_{YYYY-MM-DD_HH-MM-SS}.saver.txt`.

### AI instructions

To work on AI R&D, you must only edit the train.py file, and before every edit, you must run the saver.py script to backup the file.

### Logging Research
You must use the `logger.py` script to log the results of a training run by running:
```bash
python3 logger.py --research_name "research_name" --filename_in_saver "Saver_Branches/filename_{YYYY-MM-DD_HH-MM-SS}.saver.txt" --loss "0.025"
```
This will automatically save the entry in `logger_research/research_data.json`.

### AI Workflow
The AI works independently by following this loop:
Begin by saving the initial file:
0. Save the current state of `train.py` using `saver.py`.

Then begin the research loop as follows:
1. Edit `train.py` to test a new idea.
2. Run the training for a maximum of 60 seconds, the training run must NOT exceed this time.
3. Save the edited version of `train.py` using `saver.py`.
4. Log the research results using `logger.py`. (Make sure to save the exact filename of the branch that gave the loss for the current run)
5. Repeat the process and keep trying to make the loss as low as possible.