from django.db import models


class Printer(models.Model):
    class PrintCheckType(models.TextChoices):
        KITCHEN = "Kitchen"
        CLIENT = "Client"

    name = models.CharField(max_length=50, help_text="The printer's name.")
    api_key = models.CharField(max_length=255, help_text="The API access key.")
    check_type = models.CharField(
        max_length=50, choices=PrintCheckType.choices,
        help_text="The type of check."
    )
    point_id = models.IntegerField(
        help_text="The point to which the printer is connected."
    )
