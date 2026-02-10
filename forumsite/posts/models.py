from email.policy import default

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count, Q
from django.utils.text import slugify
from translate import Translator
from unidecode import unidecode
# Create your models here.


class Reactions:
    def __init__(self, likes, dislikes):
        self.user_likes = likes
        self.user_dislikes = dislikes

class PostsQuerySet(models.QuerySet):
    def with_reactions(self):
        return self.annotate(
            num_likes=Count('posts_likes', filter=Q(posts_likes__reaction_type=Like.Status.LIKED)),
            num_dislikes=Count('posts_likes', filter=Q(posts_likes__reaction_type=Like.Status.DISLIKED)),
        )

class PublishedManager(models.Manager):
    def get_queryset(self):
        return PostsQuerySet(self.model, using=self._db).filter(is_published=Posts.Status.PUBLISHED)

class Posts(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликована'
    title = models.CharField(max_length=100, blank=False, null=False, verbose_name='Заголовок')
    slug = models.SlugField(max_length=100, blank=False, null=False, verbose_name='Слаг')
    content = models.TextField(blank=False, null=False, verbose_name='Текст статьи')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания', null = True)
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Время обновления', null = True)
    is_published = models.BooleanField(default=Status.DRAFT, verbose_name='Статус публикации')
    tags = models.ManyToManyField('Tags', blank=True, related_name='posts', verbose_name='Тэги')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts', null=True, default=None, verbose_name='Автор')
    likes = models.ManyToManyField(get_user_model(), through='Like', blank=True, related_name='liked_posts', verbose_name='Лайки')

    # objects = models.Manager()
    objects = PostsQuerySet.as_manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property #чтобы можно было использовать как метод в шаблоне
    def get_reactions(self):
        user_dislikes = [dislike.user for dislike in self.posts_likes.filter(reaction_type=Like.Status.DISLIKED)]
        user_likes = [like.user for like in self.posts_likes.filter(reaction_type=Like.Status.LIKED)]
        return Reactions(user_likes, user_dislikes)


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

class Like(models.Model):
    class Status(models.IntegerChoices):
        DISLIKED = -1, 'Дизлайк'
        DEFAULT = 0, 'Нет реакции'
        LIKED = 1, 'Лайк'
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, default=None)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name = 'posts_likes', null=True, default=None)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_updated = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    reaction_type = models.IntegerField(default = Status.DEFAULT, choices=Status.choices, verbose_name='Тип реакции')

    class Meta:
        unique_together = ('user', 'post')
