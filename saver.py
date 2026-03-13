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
            print(f"Error: The file '{file_path}' does not exist.")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        base_name = os.path.basename(file_path)
        new_name = f"{base_name}_{timestamp}.saver.txt"
        dest_path = os.path.join(self.backup_dir, new_name)

        try:
            shutil.copy2(file_path, dest_path)
            print(f"Backed up '{file_path}' to '{dest_path}'")
        except Exception as e:
            print(f"Error backing up file: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python saver.py <filename>")
        sys.exit(1)
        
    file_to_backup = sys.argv[1]
    saver = Saver()
    saver.backup(file_to_backup)
