import json
import os
from pathlib import Path
from django.conf import settings


def get_vite_manifest():
    """
    Загружает манифест Vite для production сборки.
    В development режиме возвращает ссылки на dev сервер.
    """
    manifest_path = Path(settings.BASE_DIR) / "static" / "vue" / ".vite" / "manifest.json"

    # В development режиме
    if settings.DEBUG and not manifest_path.exists():
        return {
            'development': True,
            'main': {
                'file': 'http://localhost:5173/src/main.js',
                'css': []
            }
        }

    # В production режиме
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        # Ищем entry point
        for key, value in manifest.items():
            if value.get('isEntry'):
                return {
                    'development': False,
                    'main': {
                        'file': f'/static/vue/{value["file"]}',
                        'css': [f'/static/vue/{css}' for css in value.get('css', [])]
                    }
                }

    # Если манифест не найден
    return {
        'development': False,
        'main': {
            'file': '',
            'css': []
        }
    }


def vite_assets(request):
    """Контекстный процессор для шаблонов Django"""
    return {
        'vite': get_vite_manifest()
    }