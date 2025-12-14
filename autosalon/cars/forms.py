from django import forms
from django.core.exceptions import ValidationError
import re
from .models import PurchaseRequest


def validate_phone_number(value):
    """Валидация номера телефона в формате +7 (XXX) XXX-XX-XX или 8XXXXXXXXXX"""
    if not value:
        return value

    # Убираем все пробелы, скобки, дефисы для проверки
    cleaned = re.sub(r'[()\s\-]', '', value)

    # Проверяем форматы
    if cleaned.startswith('+7') and len(cleaned) == 12:
        # +7XXXXXXXXXX
        if not re.match(r'^\+7\d{10}$', cleaned):
            raise ValidationError('Неверный формат номера телефона. Используйте +7XXXXXXXXXX')
    elif cleaned.startswith('8') and len(cleaned) == 11:
        # 8XXXXXXXXXX
        if not re.match(r'^8\d{10}$', cleaned):
            raise ValidationError('Неверный формат номера телефона. Используйте 8XXXXXXXXXX')
    else:
        raise ValidationError('Номер телефона должен начинаться с +7 или 8 и содержать 11 цифр')

    return value


class PurchaseRequestForm(forms.ModelForm):
    """Форма для создания заявки на покупку"""

    contact_phone = forms.CharField(
        max_length=20,
        label='Телефон',
        validators=[validate_phone_number],
        widget=forms.TextInput(attrs={
            'placeholder': '+7 (999) 123-45-67',
            'class': 'phone-input'
        })
    )

    class Meta:
        model = PurchaseRequest
        fields = ['contact_name', 'contact_phone', 'contact_email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Укажите удобное время для связи, вопросы по автомобилю и т.д.'
            }),
            'contact_name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'contact_email': forms.EmailInput(attrs={'placeholder': 'email@example.com'}),
        }
        labels = {
            'contact_name': 'Имя',
            'contact_email': 'Email',
            'message': 'Сообщение',
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.car = kwargs.pop('car', None)
        super().__init__(*args, **kwargs)

        # Если пользователь авторизован, предзаполняем данные
        if self.user and self.user.is_authenticated:
            self.fields['contact_name'].initial = self.user.get_full_name() or self.user.username
            self.fields['contact_email'].initial = self.user.email
            self.fields['contact_phone'].initial = self.user.phone_number


class PurchaseRequestUpdateForm(forms.ModelForm):
    """Форма для обновления заявки (для менеджеров)"""

    class Meta:
        model = PurchaseRequest
        fields = ['status', 'manager_comment']
        widgets = {
            'manager_comment': forms.Textarea(attrs={'rows': 3}),
        }