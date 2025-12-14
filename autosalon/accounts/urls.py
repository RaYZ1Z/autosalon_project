from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Регистрация
    path('signup/', views.SignUpView.as_view(), name='signup'),

    # Вход/выход (используем кастомные представления)
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    # Личный кабинет
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),

    # Управление заявками (для менеджеров)
    path('update-request-status/<int:request_id>/', views.update_request_status, name='update_request_status'),
]