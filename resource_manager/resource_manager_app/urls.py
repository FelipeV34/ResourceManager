"""API urls."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TechnicianViewSet, ResourceAssignmentViewSet, LoginViewSet

router = DefaultRouter()
router.register("technician", TechnicianViewSet)
router.register("resource-assignment", ResourceAssignmentViewSet)
router.register("login", LoginViewSet, basename="login")


urlpatterns = [
    path("", include(router.urls)),
]
