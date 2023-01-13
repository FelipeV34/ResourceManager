"""API views."""

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet
from .models import Technician, ResourceAssignment
from .serializers import TechnicianSerializer, ResourceAssignmentSerializer


class TechnicianViewSet(ModelViewSet):
    """Handles creating, listing, retrieving, updating and deleting technicians."""

    queryset = Technician.objects.all()  # noqa
    serializer_class = TechnicianSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    filter_backends = (SearchFilter,)
    search_fields = ("name", "last_name", "id_number", "code",)


class ResourceAssignmentViewSet(ModelViewSet):
    """Handles creating, listing, retrieving, updating and deleting resource assignments."""

    queryset = ResourceAssignment.objects.all()  # noqa
    serializer_class = ResourceAssignmentSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """Adds to a technician's quantity before creation."""
        technician = Technician.objects.get(pk=request.data["technician"])  # noqa
        technician.resource_quantity += int(request.data["quantity"])
        technician.save()
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Removes from a technician's quantity before deletion."""
        assignment = ResourceAssignment.objects.get(pk=kwargs["pk"])  # noqa
        technician = Technician.objects.get(pk=assignment.technician.pk)  # noqa
        technician.resource_quantity -= int(assignment.quantity)
        technician.save()
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Updates a technician's quantities before updating."""
        assignment = ResourceAssignment.objects.get(pk=kwargs["pk"])  # noqa
        previous_technician = Technician.objects.get(pk=assignment.technician.pk)  # noqa
        new_technician = Technician.objects.get(pk=request.data["technician"])  # noqa
        previous_technician.resource_quantity -= assignment.quantity
        new_technician.resource_quantity += int(request.data["quantity"])
        previous_technician.save()
        new_technician.save()
        return super().update(request, *args, **kwargs)


class LoginViewSet(ViewSet):
    """Handles auth tokens."""

    serializer_class = AuthTokenSerializer
    obtain_auth_token = ObtainAuthToken()

    def create(self, request):
        """Creates auth tokens on successful login."""
        return self.obtain_auth_token.as_view()(request=request._request)  # noqa
