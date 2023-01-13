from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class BranchOffice(models.Model):
    """Branch office database model."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    nit = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    creation_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        """String representation for our model's entities."""
        return self.name


class Technician(models.Model):
    """Technician database model."""
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    id_number = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    base_salary = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    branch_office = models.ForeignKey(BranchOffice, on_delete=models.PROTECT)

    def __str__(self):
        """String representation for our model's entities."""
        return f"{self.name} {self.last_name}"


class Resource(models.Model):
    """Resource database model."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        """String representation for our model's entities."""
        return self.name


class ResourceAssignment(models.Model):
    """ResourceAssignment database model."""
    assignment_date = models.DateField(auto_now_add=True)
    quantity = models.SmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.PROTECT)

    def __str__(self):
        """String representation for our model's entities."""
        return f"{self.technician}: {self.resource} - {self.quantity}"
