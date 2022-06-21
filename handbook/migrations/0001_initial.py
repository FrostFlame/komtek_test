# Generated by Django 4.0.5 on 2022-06-17 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Handbook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Наименование')),
                ('short_title', models.CharField(max_length=20, verbose_name='Короткое наименование')),
                ('description', models.TextField(verbose_name='Описание')),
                ('version', models.CharField(max_length=10, verbose_name='Версия')),
                ('begin_date', models.DateField(verbose_name='Дата начала действия')),
            ],
            options={
                'unique_together': {('id', 'version')},
            },
        ),
        migrations.CreateModel(
            name='HandbookElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, verbose_name='Код элемента')),
                ('value', models.CharField(max_length=50, verbose_name='Значение элемента')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='handbook.handbook', verbose_name='Справочник')),
            ],
        ),
    ]
