from django.shortcuts import render, get_object_or_404
from django.http import Http404
from cars.models import Car  # Импортируем модель Car из приложения cars


# Детальная страница автомобиля
def vue_car_detail(request, car_id):
    """
    Отображение детальной страницы автомобиля
    Пример URL: /car/1/
    """
    try:
        # Пробуем получить автомобиль из базы данных
        car = Car.objects.get(id=car_id)

        # Получаем изображения автомобиля
        from django.conf import settings
        images = []
        scheme = 'https' if settings.SECURE_SSL_REDIRECT else 'http'
        host = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else '127.0.0.1'
        port = ':8000' if host in ['127.0.0.1', 'localhost'] else ''
        base_url = f"{scheme}://{host}{port}"

        for image in car.images.all():
            images.append({
                'id': image.id,
                'url': f"{base_url}{image.image.url}",
                'description': image.description,
                'is_main': image.is_main
            })

        # Проверяем, добавлен ли автомобиль в избранное
        is_favorite = False
        if request.user.is_authenticated:
            from cars.models import Favorite
            is_favorite = Favorite.objects.filter(user=request.user, car=car).exists()

        # Получаем похожие автомобили (той же марки, но не проданные)
        similar_cars = Car.objects.filter(
            brand=car.brand,
            is_sold=False
        ).exclude(id=car.id).order_by('?')[:3]  # 3 случайных авто

        # Форматируем данные для шаблона
        car_data = {
            'id': car.id,
            'brand': car.brand.name if hasattr(car, 'brand') and car.brand else 'Не указан',
            'model': car.model,
            'year': car.year,
            'price': car.price,
            'mileage': car.mileage,
            'color': car.color,
            'fuel_type': car.fuel_type,
            'transmission': car.transmission if hasattr(car, 'transmission') else 'automatic',
            'description': car.description if hasattr(car,
                                                      'description') else 'Премиальный автомобиль в отличном состоянии.',
            'engine_volume': car.engine_volume if hasattr(car, 'engine_volume') else 2.0,
            'horsepower': car.horsepower if hasattr(car, 'horsepower') else 150,
            'images': images,
            'main_image': images[0]['url'] if images else None,
        }

    except Car.DoesNotExist:
        # Если автомобиль не найден в базе, используем демо-данные
        car_data = {
            'id': car_id,
            'brand': 'Mercedes-Benz',
            'model': 'E-Class',
            'year': 2023,
            'price': 6500000,
            'mileage': 15000,
            'color': 'Черный',
            'fuel_type': 'petrol',
            'transmission': 'automatic',
            'description': 'Премиальный седан бизнес-класса в идеальном состоянии. Полностью обслужен, есть все документы. Кожаный салон, панорамная крыша, система помощи при парковке.',
            'engine_volume': 2.0,
            'horsepower': 258,
        }
    except Exception as e:
        # Любая другая ошибка
        raise Http404(f"Ошибка загрузки автомобиля: {str(e)}")

    # Передаем данные в шаблон
    context = {
        'car': car_data,
        'is_favorite': is_favorite,
        'similar_cars': similar_cars,
    }

    return render(request, 'cars/car_detail.html', context)