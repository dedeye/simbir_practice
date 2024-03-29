from django.urls import include, path
from rest_framework.routers import DefaultRouter

from goods_service import views

app_name = "goods"

router = DefaultRouter()
router.register(r"advert", views.AdvertView)
router.register(r"img", views.AdvertImageView)


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
    path("advert/<int:id>/img/", views.AdvertImageUpload.as_view()),
]
