import argparse
import json
import os
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Log training results.")
    parser.add_argument("--research_name", required=True, help="Name of the research project")
    parser.add_argument("--filename_in_saver", required=True, help="Path to the saved branch file")
    parser.add_argument("--loss", required=True, type=float, help="Loss value from training")
    args = parser.parse_args()

    log_dir = "logger_research"
    os.makedirs(log_dir, exist_ok=True)
    
    json_path = os.path.join(log_dir, "research_data.json")
    
    data = []
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
            
    if not isinstance(data, list):
        data = []

    # Create the log entry
    entry = {
        "timestamp": datetime.now().isoformat(),
        "research_name": args.research_name,
        "filename_in_saver": args.filename_in_saver,
        "loss": args.loss
    }
    
    data.append(entry)
    
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)
        
    print(f"Logged {args.research_name} result with loss {args.loss} to {json_path}")

if __name__ == "__main__":
    main()
