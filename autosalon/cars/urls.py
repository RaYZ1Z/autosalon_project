from django.urls import path
from . import views

app_name = 'cars'

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),

    # Детальная страница автомобиля
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),

    # Заявки на покупку
    path('purchase-requests/', views.purchase_request_list, name='purchase_request_list'),
    path('purchase-requests/<int:pk>/', views.purchase_request_detail, name='purchase_request_detail'),
    path('purchase-requests/<int:pk>/update/', views.update_purchase_request, name='purchase_request_update'),
    path('car/<int:car_id>/create-request/', views.create_purchase_request, name='create_purchase_request'),
]