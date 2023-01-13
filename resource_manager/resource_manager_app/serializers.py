"""API serializers."""

from rest_framework.serializers import ModelSerializer
from .models import Technician, ResourceAssignment


class TechnicianSerializer(ModelSerializer):
    """Technician serializer."""

    class Meta:
        model = Technician
        fields = ("id", "name", "last_name", "id_number", "code", "description", "resource_quantity", "creation_date",
                  "active", "base_salary", "branch_office",)
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
            "creation_date": {
                "read_only": True,
            },
            "resource_quantity": {
                "read_only": True,
            },
        }


class ResourceAssignmentSerializer(ModelSerializer):
    """ResourceAssignment serializer."""

    class Meta:
        model = ResourceAssignment
        fields = ("id", "assignment_date", "quantity", "technician", "resource",)
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
        }
