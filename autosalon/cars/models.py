from django.db import models

# Create your models here.

class Brand(models.Model):
    """Модель для марок автомобилей"""
    name = models.CharField(max_length=100, verbose_name="Название марки")
    country = models.CharField(max_length=50, verbose_name="Страна производитель", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    founded_year = models.IntegerField(verbose_name="Год основания", null=True, blank=True)

    class Meta:
        verbose_name = "Марка автомобиля"
        verbose_name_plural = "Марки автомобилей"
        ordering = ['name']  # сортировка по названию

    def __str__(self):
        return self.name


class Car(models.Model):
    """Модель для автомобилей"""

    # Типы коробки передач
    TRANSMISSION_CHOICES = [
        ('manual', 'Механическая'),
        ('automatic', 'Автоматическая'),
        ('robot', 'Роботизированная'),
        ('variator', 'Вариатор'),
    ]

    # Типы топлива
    FUEL_CHOICES = [
        ('petrol', 'Бензин'),
        ('diesel', 'Дизель'),
        ('electric', 'Электрический'),
        ('hybrid', 'Гибрид'),
    ]

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        verbose_name="Марка",
        related_name='cars_image'
    )
    model = models.CharField(max_length=100, verbose_name="Модель")
    year = models.IntegerField(verbose_name="Год выпуска")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )
    mileage = models.IntegerField(verbose_name="Пробег (км)", default=0)
    color = models.CharField(max_length=50, verbose_name="Цвет")
    transmission = models.CharField(
        max_length=20,
        choices=TRANSMISSION_CHOICES,
        verbose_name="Коробка передач"
    )
    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_CHOICES,
        verbose_name="Тип топлива"
    )
    engine_volume = models.FloatField(verbose_name="Объем двигателя (л)")
    horsepower = models.IntegerField(verbose_name="Лошадиные силы")
    is_sold = models.BooleanField(default=False, verbose_name="Продан")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ['-created_at']  # новые сверху

    def __str__(self):
        return f"{self.brand.name} {self.model} ({self.year})"


class CarImage(models.Model):
    """Модель для фотографий автомобилей"""
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        verbose_name="Автомобиль",
        related_name='images'
    )
    image = models.ImageField(
        upload_to='car_images/',
        verbose_name="Фотография"
    )
    description = models.CharField(
        max_length=200,
        verbose_name="Описание фото",
        blank=True
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name="Основное фото"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки"
    )

    class Meta:
        verbose_name = "Фотография автомобиля"
        verbose_name_plural = "Фотографии автомобилей"
        ordering = ['-is_main', 'uploaded_at']

    def __str__(self):
        return f"Фото {self.car.brand.name} {self.car.model}"