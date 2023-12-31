from django.db import models
from django.utils import timezone

<<<<<<< HEAD
from core.models import User
=======
from core.models import User
>>>>>>> e91189b (Initial commit)


class DatesModelMixin(models.Model):
    """
    Базовый класс модели. Сохраняет дату создания или обновления
    """
    class Meta:
        abstract = True

    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.updated = timezone.now()
        return super().save(*args, **kwargs)


class Board(DatesModelMixin):
    """
    Класс шеринг доски
    """
    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"


class BoardParticipant(DatesModelMixin):
    """
    Класс участников шеринг доски
    """
    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    board = models.ForeignKey(
        Board,
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="participants",
    )

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        related_name="participants",
    )

    role = models.PositiveSmallIntegerField(
        verbose_name="Роль",
        choices=Role.choices,
        default=Role.owner)

    editable_choices = Role.choices[1:]

    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"


class GoalCategory(DatesModelMixin):
    """
    Модель категорий для целей.
    """
    board = models.ForeignKey(Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="categories")
    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Goal(DatesModelMixin):
    """
    Модель целей
    """

    class Status(models.IntegerChoices):
        """
        Класс статуса для целей
        """
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "Архив"

    class Priority(models.IntegerChoices):
        """
        Класс приоритета для целей
        """
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    description = models.TextField(verbose_name="Описание", blank=True)
    category = models.ForeignKey(GoalCategory, verbose_name="Категория", on_delete=models.PROTECT)
    due_date = models.DateTimeField(verbose_name="Дата выполнения", null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус", choices=Status.choices, default=Status.to_do
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name="Приоритет", choices=Priority.choices, default=Priority.medium
    )

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"


class GoalComments(DatesModelMixin):
    """
    Модель комментариев для целей
    """
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    text = models.TextField(verbose_name="Текст")
    goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

