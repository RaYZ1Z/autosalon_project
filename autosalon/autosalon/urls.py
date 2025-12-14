from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView

# Импортируем наши views
from . import views  # Это импорт views из текущей папки

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', TemplateView.as_view(template_name='vue_cars.html'), name='home'),
    path('cars/', include('cars.urls')),
    path('api/', include('api.urls')),

    # Vue страницы через TemplateView
    path('vue-test/', TemplateView.as_view(template_name='vue_test.html'), name='vue_test'),
    path('vue-cars/', TemplateView.as_view(template_name='vue_cars.html'), name='vue_cars'),

    # Главная страница Vue
    path('vue-main/', TemplateView.as_view(template_name='vue_main.html'), name='vue_main'),

    # НОВЫЕ СТРАНИЦЫ (добавьте эти 4 строки):
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('login/', RedirectView.as_view(url='/accounts/login/', permanent=False), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),

    # Детальная страница автомобиля
    path('car/<int:car_id>/', views.vue_car_detail, name='vue_car_detail'),
]

# Добавляем обработку медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)