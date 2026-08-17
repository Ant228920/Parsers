import os
import sys
import django

# 1. Прописуємо шлях до головної папки проєкту
sys.path.append(r'D:\Parsers\braincomua_project')

# 2. Вказуємо, де лежать налаштування (settings.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'braincomua_project.settings')

# 3. Запускаємо ініціалізацію Django
django.setup()