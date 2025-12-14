from rest_framework import serializers
from cars.models import Car, Brand, PurchaseRequest, Favorite
from accounts.models import CustomUser


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'country', 'description']


class CarSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        source='brand',
        write_only=True
    )
    images = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = [
            'id', 'brand', 'brand_id', 'model', 'year', 'price',
            'color', 'transmission', 'fuel_type', 'engine_volume',
            'horsepower', 'mileage', 'is_sold', 'created_at', 'images', 'is_favorite'
        ]
        read_only_fields = ['created_at']

    def get_images(self, obj):
        from django.conf import settings
        request = self.context.get('request')
        base_url = ''
        if request:
            try:
                base_url = request.build_absolute_uri('/').rstrip('/')
            except:
                # Fallback to settings
                scheme = 'https' if settings.SECURE_SSL_REDIRECT else 'http'
                host = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost:8000'
                base_url = f"{scheme}://{host}"
        else:
            scheme = 'https' if settings.SECURE_SSL_REDIRECT else 'http'
            host = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else '127.0.0.1'
            port = ':8000' if host in ['127.0.0.1', 'localhost'] else ''
            base_url = f"{scheme}://{host}{port}"

        return [
            {
                'id': image.id,
                'image': f"{base_url}{image.image.url}",
                'description': image.description,
                'is_main': image.is_main
            }
            for image in obj.images.all()
        ]

    def get_is_favorite(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, car=obj).exists()
        return False


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор для избранных автомобилей"""
    car = CarSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'car', 'added_at']
        read_only_fields = ['id', 'added_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number', 'role']


class PurchaseRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    car = CarSerializer(read_only=True)
    car_id = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all(),
        source='car',
        write_only=True
    )

    class Meta:
        model = PurchaseRequest
        fields = [
            'id', 'user', 'car', 'car_id', 'contact_name',
            'contact_phone', 'contact_email', 'message',
            'status', 'manager_comment', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']