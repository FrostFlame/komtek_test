"""models"""
from django.db import models


# Create your models here.


class Handbook(models.Model):
    """Модель справочника."""
    """Глобальный идентификатор для всех версий одного справочника"""
    identifier = models.UUIDField(verbose_name='Идентификатор')
    title = models.CharField(max_length=50, verbose_name='Наименование')
    short_title = models.CharField(
        max_length=20,
        verbose_name='Короткое наименование'
    )
    description = models.TextField(verbose_name='Описание')
    version = models.CharField(
        max_length=10,
        null=False,
        blank=False,
        verbose_name='Версия'
    )
    begin_date = models.DateField(verbose_name='Дата начала действия')

    class Meta:
        """Уникальность версии в пределах одного справочника."""
        unique_together = ('identifier', 'version',)

    def __str__(self):
        return f'{self.title}: {self.version}'


class HandbookElement(models.Model):
    """Модель Элемент справочника."""
    handbook = models.ForeignKey(
        Handbook,
        related_name='elements',
        on_delete=models.CASCADE,
        blank=False, null=False,
        verbose_name='Справочник'
    )
    parent_identifier = models.UUIDField(
        verbose_name='Родительский идентификатор'
    )
    code = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name='Код элемента'
    )
    value = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name='Значение элемента'
    )

    def __str__(self):
        return self.value
