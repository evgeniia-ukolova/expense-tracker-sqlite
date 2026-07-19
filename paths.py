# файл с путями проекта

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent              # Определяет папку, в которой находится сам файл paths.py. То есть папку проекта

DATABASE_PATH = BASE_DIR / "expenses.db"                # Создаёт полный путь к базе данных
CSV_PATH = BASE_DIR / "expenses.csv"

BACKUPS_DIR = BASE_DIR / "backups"
BACKUP_PATH = BACKUPS_DIR / "expenses_backup.db"