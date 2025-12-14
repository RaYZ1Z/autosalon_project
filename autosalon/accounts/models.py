from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Роли пользователей
    ROLE_CHOICES = (
        ('client', 'Клиент'),
        ('manager', 'Менеджер'),
        ('admin', 'Администратор'),
    )

    # Дополнительные поля
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Номер телефона'
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='client',
        verbose_name='Роль'
    )

    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        verbose_name='Аватар'
    )

    registration_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата регистрации',
        editable=False
    )

    # Дополнительные поля для менеджеров/администраторов
    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Отдел'
    )

    position = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Должность'
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_manager(self):
        """Проверка, является ли пользователь менеджером"""
        return self.role in ['manager', 'admin']

    def is_admin(self):
        """Проверка, является ли пользователь администратором"""
        return self.role == 'admin'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']