from django.db import models  # ← добавьте эту строку
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Car, Brand, PurchaseRequest, Favorite
from .forms import PurchaseRequestForm, PurchaseRequestUpdateForm


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

    # --- ПОИСК ПО МОДЕЛИ И МАРКЕ ---
    search_query = request.GET.get('search', '')
    if search_query:
        cars = cars.filter(
            models.Q(model__icontains=search_query) |
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
        similar_cars = list(Car.objects.filter(
            brand=car.brand,
            is_sold=False
        ).exclude(id=car.id).order_by('?')[:3])  # 3 случайных авто

        # Проверяем, добавлен ли автомобиль в избранное
        is_favorite = False
        if request.user.is_authenticated:
            is_favorite = Favorite.objects.filter(user=request.user, car=car).exists()

        context = {
            'car': car,
            'images': images,
            'transmission_display': transmission_display,
            'fuel_display': fuel_display,
            'similar_cars': similar_cars,
            'is_favorite': is_favorite,
        }

        return render(request, 'cars/car_detail.html', context)

    except Car.DoesNotExist:
        # Если автомобиль не найден - показываем 404
        from django.http import Http404
        raise Http404("Автомобиль не найден")


# ============ НОВЫЕ ФУНКЦИИ ДЛЯ ЗАЯВОК ============

@login_required
def create_purchase_request(request, car_id):
    """Создание заявки на покупку"""
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        form = PurchaseRequestForm(request.POST, user=request.user, car=car)
        if form.is_valid():
            purchase_request = form.save(commit=False)
            purchase_request.user = request.user
            purchase_request.car = car
            purchase_request.save()

            messages.success(request, 'Ваша заявка успешно отправлена!')
            # ИСПРАВЛЯЕМ ЭТУ СТРОКУ:
            return redirect('cars:car_detail', car_id=car.id)
    else:
        form = PurchaseRequestForm(user=request.user, car=car)

    return render(request, 'cars/purchase_request_form.html', {
        'form': form,
        'car': car
    })


@login_required
def purchase_request_list(request):
    """Список заявок пользователя"""
    if request.user.is_manager():
        # Менеджеры видят все заявки
        purchase_requests = PurchaseRequest.objects.all().select_related('user', 'car', 'car__brand')
    else:
        # Обычные пользователи видят только свои заявки
        purchase_requests = PurchaseRequest.objects.filter(user=request.user).select_related('car', 'car__brand')

    # Подсчитываем статистику по статусам
    total_requests = purchase_requests.count()
    pending_requests = purchase_requests.filter(status='new').count()
    approved_requests = purchase_requests.filter(status='approved').count()
    rejected_requests = purchase_requests.filter(status='rejected').count()

    return render(request, 'cars/purchase_request_list.html', {
        'purchase_requests': purchase_requests,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests,
    })


@login_required
def purchase_request_detail(request, pk):
    """Детальная страница заявки"""
    if request.user.is_manager():
        # Менеджеры видят все заявки
        purchase_request = get_object_or_404(PurchaseRequest, pk=pk)
    else:
        # Обычные пользователи видят только свои заявки
        purchase_request = get_object_or_404(PurchaseRequest, pk=pk, user=request.user)

    # Если менеджер, добавляем форму для обновления
    update_form = None
    if request.user.is_manager():
        update_form = PurchaseRequestUpdateForm(instance=purchase_request)

    return render(request, 'cars/purchase_request_detail.html', {
        'purchase_request': purchase_request,
        'update_form': update_form
    })


@login_required
def update_purchase_request(request, pk):
    """Обновление заявки (только для менеджеров)"""
    if not request.user.is_manager():
        messages.error(request, 'У вас нет прав для выполнения этого действия')
        return redirect('cars:purchase_request_list')

    purchase_request = get_object_or_404(PurchaseRequest, pk=pk)

    if request.method == 'POST':
        form = PurchaseRequestUpdateForm(request.POST, instance=purchase_request)
        if form.is_valid():
            old_status = purchase_request.status
            form.save()

            # Отправка уведомления пользователю (если есть система уведомлений)
            try:
                from notifications.models import Notification
                new_status_display = purchase_request.get_status_display()
                old_status_display = dict(PurchaseRequest.STATUS_CHOICES)[old_status]

                message = f"Статус вашей заявки на {purchase_request.car.brand.name} {purchase_request.car.model} изменен с '{old_status_display}' на '{new_status_display}'"
                if purchase_request.manager_comment:
                    message += f". Комментарий менеджера: {purchase_request.manager_comment}"

                Notification.objects.create(
                    user=purchase_request.user,
                    title='Изменение статуса заявки',
                    message=message,
                    notification_type='request_status_update'
                )
            except ImportError:
                pass  # Если модуль уведомлений не найден, пропускаем

            messages.success(request, 'Заявка успешно обновлена')
            return redirect('cars:purchase_request_detail', pk=pk)
    else:
        form = PurchaseRequestUpdateForm(instance=purchase_request)

    return render(request, 'cars/purchase_request_update.html', {
        'form': form,
        'purchase_request': purchase_request
    })