# test_tags.py
import os
import sys

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'autosalon.settings')

import django
django.setup()

# Проверяем теги
from django.template import engines

django_engine = engines['django']
template_libs = django_engine.engine.template_libraries

print("=== ЗАРЕГИСТРИРОВАННЫЕ БИБЛИОТЕКИ ТЕГОВ ===")
for lib_name in sorted(template_libs.keys()):
    print(f"✅ {lib_name}")

print("\n=== ПРОВЕРКА cars_extras ===")
try:
    lib = template_libs.get('cars_extras')
    if lib:
        print("✅ cars_extras найден!")
        print(f"   Путь: {lib.__file__}")
    else:
        print("❌ cars_extras НЕ найден в зарегистрированных библиотеках")
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("\n=== СТРУКТУРА ПАПОК ===")
import os
for root, dirs, files in os.walk('cars'):
    level = root.replace('cars', '').count(os.sep)
    indent = ' ' * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        if file.endswith('.py'):
            print(f"{subindent}{file}")