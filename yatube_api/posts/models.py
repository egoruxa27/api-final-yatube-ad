from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        "Название группы",
        max_length=60,
    )
    slug = models.SlugField("Слаг группы", max_length=60, unique=True)
    description = models.TextField("Описанние группы")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follows",
        verbose_name="Подписчик",
        help_text="""Укажите имя пользователя который
        подпишется на другого пользователя""",
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followers",
        verbose_name="Пользователь",
        help_text="""Укажите имя пользователя
         на которого хотите подписаться""",
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "following"], name="unique_follow")
        ]


class Post(models.Model):
    text = models.TextField("Текс поста")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор"
    )
    image = models.ImageField(
        upload_to="posts/",
        null=True, blank=True,
        verbose_name="Изображение"
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name="Группа",
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-pub_date"]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комменатрия",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пост",
        help_text="""
        укажите id поста на
         который хотите оставить комментарий""",
    )
    text = models.TextField("Текст комментария")
    created = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
