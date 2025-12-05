# clear_cache.py
import os
import shutil

print("Очистка кэша Django...")

count_pyc = 0
count_cache = 0

# Удаляем .pyc файлы
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.pyc'):
            try:
                os.remove(os.path.join(root, file))
                count_pyc += 1
            except:
                pass

# Удаляем __pycache__ папки
for root, dirs, files in os.walk('.'):
    for dir_name in dirs:
        if dir_name == '__pycache__':
            try:
                shutil.rmtree(os.path.join(root, dir_name))
                count_cache += 1
            except:
                pass

print(f"Удалено: {count_pyc} .pyc файлов и {count_cache} папок __pycache__")
print("Готово!")