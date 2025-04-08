import os

# 1. Buat folder proyek secara manual di luar script ini
PROJECT_NAME = "asset_management"
os.makedirs(PROJECT_NAME, exist_ok=True)

# 2. Buat virtual environment
os.system(f"python -m venv {PROJECT_NAME}/env")

# 3. Instal Django di dalam virtual environment
os.system(f"{PROJECT_NAME}/env/Scripts/activate && pip install django")

# 4. Buat proyek Django tanpa folder tambahan
os.system(f"{PROJECT_NAME}/env/Scripts/activate && django-admin startproject core {PROJECT_NAME}")

# 5. Buat aplikasi 'assets'
os.system(f"{PROJECT_NAME}/env/Scripts/activate && cd {PROJECT_NAME} && python manage.py startapp assets")

print("Proyek Django berhasil dibuat dengan struktur dasar!")