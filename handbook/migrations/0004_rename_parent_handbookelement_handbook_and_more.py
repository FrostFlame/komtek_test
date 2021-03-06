# Generated by Django 4.0.5 on 2022-06-19 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handbook', '0003_alter_handbook_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='handbookelement',
            old_name='parent',
            new_name='handbook',
        ),
        migrations.AddField(
            model_name='handbookelement',
            name='parent_identifier',
            field=models.UUIDField(default=1, verbose_name='Родительский идентификатор'),
            preserve_default=False,
        ),
    ]
