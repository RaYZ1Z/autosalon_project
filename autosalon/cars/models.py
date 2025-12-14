from django.db import models

class Brand(models.Model):
    """Модель для марок автомобилей"""
    name = models.CharField(max_length=100, verbose_name="Название марки")
    country = models.CharField(max_length=50, verbose_name="Страна производитель", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    founded_year = models.IntegerField(verbose_name="Год основания", null=True, blank=True)

    class Meta:
        verbose_name = "Марка автомобиля"
        verbose_name_plural = "Марки автомобилей"
        ordering = ['name']

    def __str__(self):
        return self.name


class Car(models.Model):
    """Модель для автомобилей"""

    TRANSMISSION_CHOICES = [
        ('manual', 'Механическая'),
        ('automatic', 'Автоматическая'),
        ('robot', 'Роботизированная'),
        ('variator', 'Вариатор'),
    ]

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
        related_name='cars'  # <-- ИСПРАВЛЕНО: 'cars' вместо 'cars_image'
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
        ordering = ['-created_at']

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


class Favorite(models.Model):
    """Модель избранных автомобилей пользователя"""
    user = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Автомобиль'
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        ordering = ['-added_at']
        unique_together = ['user', 'car']  # Один пользователь может добавить авто в избранное только один раз

    def __str__(self):
        return f"{self.user.username} - {self.car}"


class PurchaseRequest(models.Model):
    """Модель заявки на покупку автомобиля"""

    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('in_progress', 'В обработке'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
        ('completed', 'Завершена'),
    )

    # Связь с пользователем (кто оставил заявку)
    user = models.ForeignKey(
        'accounts.CustomUser',  # Используем строку чтобы избежать циклических импортов
        on_delete=models.CASCADE,
        related_name='purchase_requests',
        verbose_name='Пользователь'
    )

    # Связь с автомобилем
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='purchase_requests',
        verbose_name='Автомобиль'
    )

    # Контактные данные (дублируем на случай если пользователь их изменит)
    contact_name = models.CharField(max_length=100, verbose_name='Имя')
    contact_phone = models.CharField(max_length=20, verbose_name='Телефон')
    contact_email = models.EmailField(verbose_name='Email')

    # Сообщение от пользователя
    message = models.TextField(blank=True, verbose_name='Сообщение')

    # Статус заявки
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )

    # Комментарий менеджера
    manager_comment = models.TextField(blank=True, verbose_name='Комментарий менеджера')

    # Даты
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Заявка на покупку'
        verbose_name_plural = 'Заявки на покупку'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        return f"Заявка #{self.id} на {self.car} от {self.contact_name}"

    def can_be_edited_by_user(self, user):
        """Может ли пользователь редактировать заявку"""
        return user == self.user and self.status in ['new', 'in_progress']

    def can_be_processed_by_user(self, user):
        """Может ли пользователь обрабатывать заявку (менеджер/админ)"""
        return user.is_manager() and self.status != 'completed'