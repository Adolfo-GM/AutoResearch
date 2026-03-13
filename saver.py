import os
import shutil
import sys
from datetime import datetime

class Saver:
    def __init__(self, backup_dir="Saver_Branches"):
        self.backup_dir = backup_dir
        os.makedirs(self.backup_dir, exist_ok=True)

    def backup(self, file_path):
        if not os.path.isfile(file_path):
            return
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        name = os.path.basename(file_path)
        dest = os.path.join(self.backup_dir, f"{name}_{ts}.saver.txt")
        try:
            shutil.copy2(file_path, dest)
            print(f"Backed up {file_path} to {dest}")
        except:
            pass

    def restore(self, backup_path, target_path="train.py"):
        if not os.path.isfile(backup_path):
            return
        try:
            shutil.copy2(backup_path, target_path)
            print(f"Restored {backup_path} to {target_path}")
        except:
            pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    
    saver = Saver()
    if sys.argv[1] == "--restore" and len(sys.argv) > 2:
        saver.restore(sys.argv[2])
    else:
        saver.backup(sys.argv[1])
