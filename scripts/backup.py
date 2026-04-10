import subprocess
import shutil
import os
import dotenv
from datetime import datetime

dotenv.load_dotenv()

backup_dir = os.path.join(os.path.dirname(__file__), "..", "backups")
os.makedirs(backup_dir, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    filename = f"backup_{timestamp}.sql"
    output_path = os.path.join(backup_dir, filename)
    print(f"PostgreSQL detected. Backing up to {filename}...")
    result = subprocess.run(["pg_dump", DATABASE_URL, "-f", output_path])
    if result.returncode == 0:
        print(f"Backup saved: {filename}")
    else:
        print("Backup failed. Make sure pg_dump is installed and DATABASE_URL is correct.")
else:
    sqlite_path = os.path.join(os.path.dirname(__file__), "..", "portfolio.db")
    if not os.path.exists(sqlite_path):
        print("ERROR: No portfolio.db found and DATABASE_URL is not set.")
        exit(1)
    filename = f"backup_{timestamp}.db"
    output_path = os.path.join(backup_dir, filename)
    print(f"SQLite detected. Backing up to {filename}...")
    shutil.copy2(sqlite_path, output_path)
    print(f"Backup saved: {filename}")
