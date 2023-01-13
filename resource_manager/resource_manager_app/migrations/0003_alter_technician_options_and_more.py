# Generated by Django 4.1.5 on 2023-01-13 02:34

import django.core.validators
from django.db import migrations, models
import resource_manager_app.utils


class Migration(migrations.Migration):

    dependencies = [
        ("resource_manager_app", "0002_alter_resourceassignment_unique_together"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="technician",
            options={"ordering": ["-active", "creation_date"]},
        ),
        migrations.AddField(
            model_name="technician",
            name="resource_quantity",
            field=models.SmallIntegerField(
                default=0, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AlterField(
            model_name="branchoffice",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="resource",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="technician",
            name="code",
            field=models.CharField(
                max_length=255,
                validators=[resource_manager_app.utils.letter_number_only_validator],
            ),
        ),
        migrations.AlterField(
            model_name="technician",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
