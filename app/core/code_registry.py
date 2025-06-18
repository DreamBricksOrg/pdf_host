import csv
import os
from threading import Lock
from datetime import datetime

FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'used_codes.csv')
registry_lock = Lock()
used_codes = {}

def load_used_codes():
    global used_codes
    used_codes = {}
    if not os.path.exists(FILE_PATH):
        return

    with open(FILE_PATH, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                project_id, code = row[0], row[1]
                used_codes.setdefault(project_id, set()).add(code)

def is_code_used(project_id: str, code: str) -> bool:
    with registry_lock:
        return code in used_codes.get(project_id, set())

def mark_code_used(project_id: str, code: str):
    with registry_lock:
        used_codes.setdefault(project_id, set()).add(code)
        with open(FILE_PATH, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            timestamp = datetime.now().isoformat()
            writer.writerow([project_id, code, timestamp])
