"""API urls."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TechnicianViewSet, ResourceAssignmentViewSet, LoginViewSet, CreateTechnicanApiView

router = DefaultRouter()
router.register("technician", TechnicianViewSet)
router.register("resource-assignment", ResourceAssignmentViewSet)
router.register("login", LoginViewSet, basename="login")


urlpatterns = [
    path("new-technician", CreateTechnicanApiView.as_view()),
    path("", include(router.urls)),
]
