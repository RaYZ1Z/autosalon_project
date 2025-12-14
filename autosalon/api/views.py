from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from cars.models import Car, PurchaseRequest, Favorite
from accounts.models import CustomUser
from .serializers import (
    CarSerializer,
    PurchaseRequestSerializer,
    UserSerializer,
    FavoriteSerializer
)


class CarViewSet(viewsets.ModelViewSet):
    """API для автомобилей"""
    queryset = Car.objects.filter(is_sold=False).select_related('brand')
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    @method_decorator(csrf_exempt, name='dispatch')
    def create_request(self, request, pk=None):
        """Создание заявки на автомобиль"""
        car = self.get_object()
        serializer = PurchaseRequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, car=car)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseRequestViewSet(viewsets.ModelViewSet):
    """API для заявок"""
    serializer_class = PurchaseRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Пользователи видят свои заявки, менеджеры - все"""
        user = self.request.user
        if user.is_manager():
            return PurchaseRequest.objects.all().select_related('user', 'car')
        return PurchaseRequest.objects.filter(user=user).select_related('car')

    def perform_create(self, serializer):
        """Автоматически привязываем пользователя"""
        serializer.save(user=self.request.user)


class FavoriteViewSet(viewsets.ModelViewSet):
    """API для избранных автомобилей"""
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('car')

    def perform_create(self, serializer):
        car_id = self.request.data.get('car_id')
        car = get_object_or_404(Car, id=car_id)
        # Проверяем, не добавлен ли уже в избранное
        if not Favorite.objects.filter(user=self.request.user, car=car).exists():
            serializer.save(user=self.request.user, car=car)
        else:
            # Если уже есть, возвращаем ошибку
            raise serializers.ValidationError("Автомобиль уже в избранном")

    @action(detail=False, methods=['post'])
    @method_decorator(csrf_exempt, name='dispatch')
    def toggle(self, request):
        """Добавить/удалить из избранного"""
        car_id = request.data.get('car_id')
        car = get_object_or_404(Car, id=car_id)

        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            car=car
        )

        if not created:
            favorite.delete()
            return Response({'action': 'removed', 'message': 'Удалено из избранного'})

        return Response({'action': 'added', 'message': 'Добавлено в избранное'})

    @action(detail=True, methods=['get'])
    def check(self, request, pk=None):
        """Проверить, добавлен ли автомобиль в избранное"""
        car = get_object_or_404(Car, id=pk)
        is_favorite = Favorite.objects.filter(user=request.user, car=car).exists()
        return Response({'is_favorite': is_favorite})


class LoginView(APIView):
    """API для входа в систему"""
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Необходимо указать username и password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            serializer = UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            })
        else:
            return Response(
                {'error': 'Неверные учетные данные'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class RegisterView(APIView):
    """API для регистрации"""
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number', '')

        if not username or not email or not password:
            return Response(
                {'error': 'Необходимо указать username, email и password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if CustomUser.objects.filter(username=username).exists():
            return Response(
                {'error': 'Пользователь с таким именем уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if CustomUser.objects.filter(email=email).exists():
            return Response(
                {'error': 'Пользователь с таким email уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone_number=phone_number,
            role='client'
        )

        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)


class CurrentUserView(APIView):
    """API для получения текущего пользователя"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)