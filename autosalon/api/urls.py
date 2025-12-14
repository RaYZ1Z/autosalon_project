from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'cars', views.CarViewSet)
router.register(r'purchase-requests', views.PurchaseRequestViewSet, basename='purchaserequest')
router.register(r'favorites', views.FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
    path('current-user/', views.CurrentUserView.as_view(), name='current-user'),
    path('auth/login/', views.LoginView.as_view(), name='api-login'),
    path('auth/register/', views.RegisterView.as_view(), name='api-register'),
    path('auth/', include('rest_framework.urls')),  # DRF login/logout
]