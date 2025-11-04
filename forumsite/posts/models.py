from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from translate import Translator
from unidecode import unidecode
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
    tags = models.ManyToManyField('Tags', blank=True, related_name='posts', verbose_name='Тэги')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts', null=True, default=None)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-time_created']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        indexes = [
            models.Index(fields=['-time_created']),
        ]

class Tags(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False, verbose_name='Тэги')
    slug = models.SlugField(max_length=100, blank=False, null=False, unique=False)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == '':
            try:
                translator = Translator(to_lang='en', from_lang='ru')
                if translator.translate(self.title) == self.title:
                    print()
                    self.slug = unidecode(self.title)
                else:
                    self.slug = translator.translate(self.title).lower()
            except Exception:
                self.slug = unidecode(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug