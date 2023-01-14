"""API views."""

from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from .models import Technician, ResourceAssignment, BranchOffice, Resource
from .serializers import CreateTechnicianSerializer, TechnicianSerializer, ResourceAssignmentSerializer


class TechnicianViewSet(ModelViewSet):
    """Handles creating, listing, retrieving, updating and deleting technicians."""

    queryset = Technician.objects.all()  # noqa
    serializer_class = TechnicianSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    filter_backends = (SearchFilter,)
    search_fields = ("name", "last_name", "id_number", "code",)

    http_method_names = ["get", "put", "patch", "delete", "head", "options", "trace"]


class CreateTechnicanApiView(CreateAPIView):
    """
    View created specifically to create new technicians receiving a customized object with resources already assigned.
    """

    serializer_class = CreateTechnicianSerializer

    def post(self, request, *args, **kwargs):
        """Creates a new technician and assigns the given resources."""

        serializer = CreateTechnicianSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError("The given body may contain errors.")

        new_technician = Technician(
            name=serializer["name"].value,
            last_name=serializer["last_name"].value,
            id_number=serializer["id_number"].value,
            code=serializer["code"].value,
            description=serializer["description"].value,
            base_salary=serializer["base_salary"].value,
            branch_office=BranchOffice.objects.get(pk=serializer["branch_office"].value),  # noqa
            resource_quantity=sum([item["quantity"] for item in serializer["assigned_resources"].value])
        )

        try:
            new_technician.save()
            for resource_serializer in serializer["assigned_resources"].value:
                assignment = ResourceAssignment(
                    quantity=resource_serializer["quantity"],
                    technician=new_technician,
                    resource=Resource.objects.get(pk=resource_serializer["id"])  # noqa
                )
                assignment.save()

        except Exception:
            if new_technician.pk is not None:
                new_technician.delete()
            raise ValidationError("The given body may contain errors.")

        return Response(data={"detail": "Technician created and resources assigned successfully."})


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
        assignment_quantity = int(assignment.quantity)
        if technician.resource_quantity - assignment_quantity < 1:
            raise ValidationError("Technicians cannot have 0 resources assigned.")
        technician.resource_quantity -= assignment_quantity
        technician.save()
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Updates a technician's quantities before updating."""
        new_quantity = int(request.data["quantity"])
        if new_quantity < 1 or new_quantity > 10:
            raise ValidationError("Invalid quantity.")

        assignment = ResourceAssignment.objects.get(pk=kwargs["pk"])  # noqa
        previous_technician = Technician.objects.get(pk=assignment.technician.pk)  # noqa
        new_technician = Technician.objects.get(pk=request.data["technician"])  # noqa

        previous_quantity = assignment.quantity
        if previous_technician == new_technician:
            previous_technician.resource_quantity += new_quantity - previous_quantity
            previous_technician.save()
            return super().update(request, *args, **kwargs)

        if previous_technician.resource_quantity - previous_quantity < 1:
            raise ValidationError("Technicians cannot have 0 resources assigned.")

        previous_technician.resource_quantity -= previous_quantity
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
