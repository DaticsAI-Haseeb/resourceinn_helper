from django.urls import re_path, include
from rest_framework import routers

from user.views import UserViewSet, LogViewSet

app_name = "user"

router = routers.DefaultRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"log", LogViewSet, basename="log")

urlpatterns = [
    re_path(r"^", include(router.urls)),
]

urlpatterns += router.urls
