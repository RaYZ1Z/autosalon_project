from django.contrib import admin
from .models import Brand, Car, CarImage

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