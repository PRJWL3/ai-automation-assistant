from fastapi import FastAPI
from datetime import datetime
import json
import os

app = FastAPI()

TASK_FILE = "tasks.json"

# Ensure file exists
if not os.path.exists(TASK_FILE):
    with open(TASK_FILE, "w") as f:
        json.dump([], f)

@app.post("/add_task")
def add_task(task: str, time: str):
    with open(TASK_FILE, "r") as f:
        data = json.load(f)

    data.append({
        "task": task,
        "time": time
    })

    with open(TASK_FILE, "w") as f:
        json.dump(data, f)

    return {"status": "task added"}