import time
import json
from datetime import datetime
import subprocess
import os

TASK_FILE = "tasks.json"

def run_worker():
    while True:
        if os.path.exists(TASK_FILE):
            with open(TASK_FILE, "r") as f:
                tasks = json.load(f)

            remaining = []

            for t in tasks:
                task_time = datetime.fromisoformat(t["time"])

                if datetime.now() >= task_time:
                    print("⏰ Triggering:", t["task"])

                    subprocess.Popen(["python", "alarm_player.py"])

                else:
                    remaining.append(t)

            with open(TASK_FILE, "w") as f:
                json.dump(remaining, f)

        time.sleep(5)

if __name__ == "__main__":
    run_worker()