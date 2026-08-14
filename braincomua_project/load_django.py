import os
import sys
import django

sys.path.append(r'D:\Parsers\braincomua_project')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'braincomua_project.settings')

django.setup()