"""API serializers."""

from rest_framework.serializers import (ModelSerializer, Serializer, CharField, FloatField, ListField, IntegerField,
                                        PrimaryKeyRelatedField)
from .models import Technician, ResourceAssignment, BranchOffice, Resource


class ResourceSerializer(Serializer):  # noqa
    """Serializer to input a resource ID and quantity."""
    id = PrimaryKeyRelatedField(queryset=Resource.objects.all())  # noqa
    quantity = IntegerField(min_value=1, max_value=10)


class CreateTechnicianSerializer(Serializer):  # noqa
    """Serializer specific to create new technicians with resources to assign to them on creation."""

    name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    id_number = CharField(max_length=255)
    code = CharField(max_length=255)
    description = CharField()
    base_salary = FloatField(min_value=0)
    branch_office = PrimaryKeyRelatedField(queryset=BranchOffice.objects.all())  # noqa
    assigned_resources = ListField(child=ResourceSerializer(), allow_empty=False)


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
