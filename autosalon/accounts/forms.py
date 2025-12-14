from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
import re
from .models import CustomUser


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


# Форма для админки
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'role')


class CustomUserChangeForm(UserChangeForm):
    """Форма для редактирования пользователя в админке"""
    class Meta:
        model = CustomUser
        exclude = ['registration_date']  # Просто исключаем поле

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поля дат только для чтения
        self.fields['registration_date'].disabled = True
        self.fields['date_joined'].disabled = True
        self.fields['last_login'].disabled = True


# Форма для регистрации на сайте (только для клиентов)
class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        label='Телефон',
        validators=[validate_phone_number],
        widget=forms.TextInput(attrs={
            'placeholder': '+7 (999) 123-45-67',
            'class': 'form-control phone-input'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']
        user.role = 'client'  # Все новые пользователи - клиенты
        if commit:
            user.save()
        return user


# Форма редактирования профиля
class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        label='Телефон',
        validators=[validate_phone_number],
        widget=forms.TextInput(attrs={
            'class': 'form-control phone-input',
            'placeholder': '+7 (999) 123-45-67'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number',
                  'profile_picture', 'department', 'position')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
        }