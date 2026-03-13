# AutoResearch

This project is intended to be a lab that allows an AI agent to run AI experiments and the validation suite allows the research to be tested and validated, all research is organized, versioned and validated. This lab allows AI to perform independent artificial intelligence research and development.

### File Backups
You can use the `saver.py` script to back up a file by running `python saver.py <filename>`. It uses a `Saver` class to automatically create a `Saver_Branches/` directory, saving a copy of the specified file with the current date and time down to the second in the format `filename_{YYYY-MM-DD_HH-MM-SS}.saver.txt`.

### AI instructions

To work on AI R&D, you must only edit the train.py file, and before every edit, you must run the saver.py script to backup the file.