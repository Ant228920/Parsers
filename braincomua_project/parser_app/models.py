from django.db import models


class Phone(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Полное название товара")
    product_code = models.CharField(max_length=100, unique=True, verbose_name="Код товара")
    manufacturer = models.CharField(max_length=100, null=True, blank=True, verbose_name="Производитель")

    color = models.CharField(max_length=100, null=True, blank=True, verbose_name="Цвет")
    memory_capacity = models.CharField(max_length=50, null=True, blank=True, verbose_name="Объем памяти")
    screen_diagonal = models.CharField(max_length=50, null=True, blank=True, verbose_name="Диагональ экрана")
    screen_resolution = models.CharField(max_length=100, null=True, blank=True, verbose_name="Разрешение дисплея")

    regular_price = models.IntegerField(null=True, blank=True, verbose_name="Цена обычная")
    promo_price = models.IntegerField(null=True, blank=True, verbose_name="Цена акционная")
    reviews_count = models.IntegerField(default=0, verbose_name="Кол-во отзывов")

    photos = models.JSONField(default=list, verbose_name="Все фото товара")
    specifications = models.JSONField(default=dict, verbose_name="Характеристики товара (словарь)")

    def __str__(self):
        return f"{self.product_code} | {self.full_name}"