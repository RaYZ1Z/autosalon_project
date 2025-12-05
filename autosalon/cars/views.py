from django.db import models  # ← добавьте эту строку
from django.shortcuts import render
from .models import Car, Brand
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    """Главная страница - список автомобилей с поиском и фильтрацией"""

    # Получаем все автомобили (которые не проданы)
    cars = Car.objects.filter(is_sold=False).select_related('brand')

    # Получаем все марки для фильтрации
    brands = Brand.objects.all()

    # Инициализируем переменные поиска
    search_query = ''
    min_price = ''
    max_price = ''
    min_year = ''
    max_year = ''

    # --- ФИЛЬТРАЦИЯ ПО МАРКЕ ---
    brand_filter = request.GET.get('brand')
    if brand_filter:
        cars = cars.filter(brand_id=brand_filter)

    # --- ПОИСК ПО МОДЕЛИ И ОПИСАНИЮ ---
    search_query = request.GET.get('search', '')
    if search_query:
        cars = cars.filter(
            models.Q(model__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(brand__name__icontains=search_query)
        )

    # --- ФИЛЬТРАЦИЯ ПО ЦЕНЕ ---
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if min_price and min_price.isdigit():
        cars = cars.filter(price__gte=int(min_price))

    if max_price and max_price.isdigit():
        cars = cars.filter(price__lte=int(max_price))

    # --- ФИЛЬТРАЦИЯ ПО ГОДУ ---
    min_year = request.GET.get('min_year', '')
    max_year = request.GET.get('max_year', '')

    if min_year and min_year.isdigit():
        cars = cars.filter(year__gte=int(min_year))

    if max_year and max_year.isdigit():
        cars = cars.filter(year__lte=int(max_year))

    # --- ФИЛЬТРАЦИЯ ПО ТИПУ КОРОБКИ ПЕРЕДАЧ ---
    transmission_filter = request.GET.get('transmission')
    if transmission_filter:
        cars = cars.filter(transmission=transmission_filter)

    # --- ФИЛЬТРАЦИЯ ПО ТИПУ ТОПЛИВА ---
    fuel_filter = request.GET.get('fuel')
    if fuel_filter:
        cars = cars.filter(fuel_type=fuel_filter)

    # Сортируем по дате добавления (новые сверху)
    cars = cars.order_by('-created_at')

    # Подсчитываем общее количество после фильтрации
    total_cars = cars.count()

    # --- ПАГИНАЦИЯ ---
    page = request.GET.get('page', 1)
    paginator = Paginator(cars, 6)  # 6 автомобилей на странице

    try:
        cars = paginator.page(page)
    except PageNotAnInteger:
        cars = paginator.page(1)
    except EmptyPage:
        cars = paginator.page(paginator.num_pages)

    # Передаем данные в шаблон
    context = {
        'cars': cars,
        'brands': brands,
        'brand_filter': brand_filter,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'min_year': min_year,
        'max_year': max_year,
        'transmission_filter': transmission_filter,
        'fuel_filter': fuel_filter,
        'total_cars': total_cars,
        'TRANSMISSION_CHOICES': Car.TRANSMISSION_CHOICES,
        'FUEL_CHOICES': Car.FUEL_CHOICES,
        'paginator': paginator,
        'page_obj': cars,
    }

    return render(request, 'cars/home.html', context)


def car_detail(request, car_id):
    """Страница с подробной информацией об автомобиле"""

    try:
        # Получаем автомобиль по ID
        car = Car.objects.select_related('brand').prefetch_related('images').get(id=car_id)

        # Получаем все фотографии этого автомобиля
        images = car.images.all()

        # Получаем основной вариант передачи (для удобства)
        transmission_display = dict(Car.TRANSMISSION_CHOICES).get(car.transmission, car.transmission)

        # Получаем основной вариант топлива (для удобства)
        fuel_display = dict(Car.FUEL_CHOICES).get(car.fuel_type, car.fuel_type)

        # Получаем похожие автомобили (той же марки, но не проданные)
        similar_cars = Car.objects.filter(
            brand=car.brand,
            is_sold=False
        ).exclude(id=car.id).order_by('?')[:3]  # 3 случайных авто

        context = {
            'car': car,
            'images': images,
            'transmission_display': transmission_display,
            'fuel_display': fuel_display,
            'similar_cars': similar_cars,
        }

        return render(request, 'cars/car_detail.html', context)

    except Car.DoesNotExist:
        # Если автомобиль не найден - показываем 404
        from django.http import Http404
        raise Http404("Автомобиль не найден")