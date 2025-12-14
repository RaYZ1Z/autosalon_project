from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class TelegramUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telegram_id = models.CharField(max_length=100, unique=True)
    chat_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)