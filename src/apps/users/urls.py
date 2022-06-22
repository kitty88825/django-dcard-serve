from django.urls import include, path
from rest_framework.routers import SimpleRouter

from apps.users.views import UserViewSet

app_name = "users"

router = SimpleRouter(False)
router.register("", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
