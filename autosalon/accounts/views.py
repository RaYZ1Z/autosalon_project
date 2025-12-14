# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomUserCreationForm, UserSignUpForm, UserProfileForm
from .models import CustomUser

class SignUpView(CreateView):
    """Регистрация нового пользователя"""
    form_class = UserSignUpForm  # Используем форму для сайта
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'  # Явно указываем шаблон

class CustomLoginView(LoginView):
    """Вход в систему"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    """Выход из системы"""
    next_page = '/'

def profile(request):
    """Просмотр профиля пользователя"""
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    # Получаем статистику пользователя
    favorites_count = request.user.favorites.count()
    favorite_cars = request.user.favorites.select_related('car', 'car__brand').order_by('-added_at')[:6]

    # Для менеджеров показываем все заявки
    if request.user.is_manager():
        from cars.models import PurchaseRequest
        all_requests = PurchaseRequest.objects.select_related('user', 'car', 'car__brand').order_by('-created_at')[:10]
        purchase_requests_count = PurchaseRequest.objects.count()
        active_requests_count = PurchaseRequest.objects.filter(status__in=['new', 'in_progress']).count()
        recent_requests = all_requests
        user_requests_count = request.user.purchase_requests.count()
        context = {
            'user': request.user,
            'purchase_requests_count': purchase_requests_count,
            'favorites_count': favorites_count,
            'active_requests_count': active_requests_count,
            'recent_requests': recent_requests,
            'favorite_cars': favorite_cars,
            'is_manager': True,
            'all_requests': all_requests,
            'user_requests_count': user_requests_count,
        }
    else:
        # Для обычных пользователей показываем только свои заявки
        purchase_requests_count = request.user.purchase_requests.count()
        active_requests_count = request.user.purchase_requests.filter(status__in=['new', 'in_progress']).count()
        recent_requests = request.user.purchase_requests.select_related('car', 'car__brand').order_by('-created_at')[:5]
        context = {
            'user': request.user,
            'purchase_requests_count': purchase_requests_count,
            'favorites_count': favorites_count,
            'active_requests_count': active_requests_count,
            'recent_requests': recent_requests,
            'favorite_cars': favorite_cars,
            'is_manager': False,
        }

    return render(request, 'accounts/profile.html', context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля"""
    model = CustomUser
    form_class = UserProfileForm  # Используем обновлённую форму
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user


def update_request_status(request, request_id):
    """Изменение статуса заявки менеджером"""
    if not request.user.is_authenticated or not request.user.is_manager():
        return JsonResponse({'error': 'Недостаточно прав'}, status=403)

    if request.method != 'POST':
        return JsonResponse({'error': 'Метод не поддерживается'}, status=405)

    from cars.models import PurchaseRequest
    purchase_request = get_object_or_404(PurchaseRequest, id=request_id)

    if not purchase_request.can_be_processed_by_user(request.user):
        return JsonResponse({'error': 'Невозможно изменить статус этой заявки'}, status=400)

    new_status = request.POST.get('status')
    manager_comment = request.POST.get('manager_comment', '')

    if new_status not in dict(PurchaseRequest.STATUS_CHOICES):
        return JsonResponse({'error': 'Неверный статус'}, status=400)

    old_status = purchase_request.status
    purchase_request.status = new_status
    purchase_request.manager_comment = manager_comment
    purchase_request.save()

    # Получаем текстовые представления статусов
    old_status_display = dict(PurchaseRequest.STATUS_CHOICES)[old_status]
    new_status_display = purchase_request.get_status_display()

    # Отправка уведомления пользователю (если есть система уведомлений)
    try:
        from notifications.models import Notification
        message = f"Статус вашей заявки на {purchase_request.car.brand.name} {purchase_request.car.model} изменен с '{old_status_display}' на '{new_status_display}'"
        if manager_comment:
            message += f". Комментарий менеджера: {manager_comment}"

        Notification.objects.create(
            user=purchase_request.user,
            title='Изменение статуса заявки',
            message=message,
            notification_type='request_status_update'
        )
    except ImportError:
        pass  # Если модуль уведомлений не найден, пропускаем

    return JsonResponse({
        'success': True,
        'new_status': new_status,
        'new_status_display': purchase_request.get_status_display(),
        'manager_comment': manager_comment
    })

    def get_form(self, form_class=None):
        """Ограничиваем редактирование роли для обычных пользователей"""
        form = super().get_form(form_class)
        # Если пользователь не админ, скрываем поле role
        if not self.request.user.is_superuser:
            if 'role' in form.fields:
                del form.fields['role']
        return form

    def get_object(self):
        return self.request.user