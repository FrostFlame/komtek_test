from django.urls import path

from handbook.views import main_page, HandbookView

app_name = 'handbook'

urlpatterns = [
    path(r'', main_page, name="main_page"),
    path(r'handbook/<int:pk>', HandbookView.as_view(), name="handbook"),
]
