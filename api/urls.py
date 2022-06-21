from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'handbooks', views.HandbookViewSet)
router.register(r'elements', views.HandbookElementViewSet)

urlpatterns = router.urls
