from django.conf import settings
from django.db import models
from django.utils import timezone

NULLABLE = {"null": True, "blank": True}

class Ad(models.Model):
    """Модель объявления"""
    title = models.CharField(max_length=150, verbose_name='название товара', default="без названия")
    price = models.PositiveIntegerField(verbose_name="цена", default=0)
    description = models.TextField(verbose_name="описание", max_length=500, **NULLABLE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="ads", on_delete=models.CASCADE,
                               verbose_name="автор", **NULLABLE)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="время создания")
    image = models.ImageField(upload_to="ads/", verbose_name="Изображение", **NULLABLE)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "объявление"
        verbose_name_plural = "объявления"
        app_label = 'ads'

    def __str__(self):
        return f'{self.title} - {self.price}'


class Comment(models.Model):
    """Модель комментария"""
    text = models.TextField(verbose_name="текст отзыва")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviews", on_delete=models.CASCADE,
                               verbose_name="автор", **NULLABLE)
    ad = models.ForeignKey(Ad, related_name="reviews", on_delete=models.CASCADE, verbose_name="объявление")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="время создания")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"

    def __str__(self):
        return f"Отзыв от {self.author} создан {self.created_at}"