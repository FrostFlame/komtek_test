from django.apps import apps
from django.contrib import admin

# Регистрация моделей для админки
for model in apps.get_app_config('handbook').models.values():
    admin.site.register(model)
