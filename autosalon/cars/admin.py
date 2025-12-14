from django.contrib import admin
from .models import Brand, Car, CarImage, PurchaseRequest  # <-- ДОБАВЛЯЕМ PurchaseRequest


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'founded_year')
    search_fields = ('name', 'country')
    list_filter = ('country',)
    ordering = ('name',)


class CarImageInline(admin.TabularInline):
    """Встроенное отображение фото в админке авто"""
    model = CarImage
    extra = 1  # количество пустых форм для добавления фото
    fields = ('image', 'description', 'is_main')
    readonly_fields = ('uploaded_at',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'brand',
        'model',
        'year',
        'price',
        'color',
        'is_sold',
        'created_at'
    )
    list_filter = (
        'brand',
        'year',
        'transmission',
        'fuel_type',
        'is_sold'
    )
    search_fields = ('model', 'color', 'brand__name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CarImageInline]  # добавляем фото прямо в форму авто

    fieldsets = (
        ('Основная информация', {
            'fields': ('brand', 'model', 'year', 'price', 'color')
        }),
        ('Технические характеристики', {
            'fields': (
                'transmission',
                'fuel_type',
                'engine_volume',
                'horsepower',
                'mileage'
            ),
            'classes': ('collapse',)  # сворачиваемый блок
        }),
        ('Статус', {
            'fields': ('is_sold',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ('car', 'image', 'is_main', 'uploaded_at')
    list_filter = ('is_main', 'uploaded_at')
    search_fields = ('car__model', 'car__brand__name', 'description')
    readonly_fields = ('uploaded_at',)
    list_editable = ('is_main',)  # можно менять прямо в списке


@admin.register(PurchaseRequest)
class PurchaseRequestAdmin(admin.ModelAdmin):
    """Админка для заявок на покупку"""

    list_display = [
        'id', 'car', 'user', 'contact_name',
        'contact_phone', 'status', 'created_at'
    ]

    list_filter = ['status', 'created_at', 'car__brand']

    search_fields = [
        'contact_name', 'contact_phone', 'contact_email',
        'user__username', 'car__model', 'car__brand__name'
    ]

    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'car', 'status')
        }),
        ('Контактные данные', {
            'fields': ('contact_name', 'contact_phone', 'contact_email')
        }),
        ('Сообщения', {
            'fields': ('message', 'manager_comment')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # Действия в админке
    actions = ['mark_as_in_progress', 'mark_as_approved', 'mark_as_rejected']

    def mark_as_in_progress(self, request, queryset):
        queryset.update(status='in_progress')
        self.message_user(request, f"{queryset.count()} заявок переведены в обработку")

    mark_as_in_progress.short_description = "Перевести в обработку"

    def mark_as_approved(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"{queryset.count()} заявок одобрены")

    mark_as_approved.short_description = "Одобрить выбранные"

    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} заявок отклонены")

    mark_as_rejected.short_description = "Отклонить выбранные"