from django.db import models

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Posts.Status.PUBLISHED)

class Posts(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликована'
    title = models.CharField(max_length=100, blank=False, null=False, verbose_name='Заголовок')
    content = models.TextField(blank=False, null=False, verbose_name='Текст статьи')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    is_published = models.BooleanField(default=Status.DRAFT, verbose_name='Статус публикации')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title
