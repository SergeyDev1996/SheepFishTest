from django.db import models


class Check(models.Model):
    class CheckTypeChoices(models.TextChoices):
        KITCHEN = "Kitchen"
        CLIENT = "Client"

    class CheckStatusChoices(models.TextChoices):
        NEW = "New"
        RENDERED = "RENDERED"
        PRINTED = "PRINTED"

    printer_id = models.ForeignKey(
        to="printer.Printer",
        related_name="printer",
        on_delete=models.CASCADE,
        help_text="The printer's ID.",
    )
    type = models.CharField(
        max_length=50, choices=CheckTypeChoices.choices, help_text="The type of check."
    )
    order = models.JSONField(help_text="The order details.")
    status = models.CharField(
        max_length=50,
        choices=CheckStatusChoices.choices,
        help_text="The check's status.",
    )
    pdf_file = models.FileField(help_text="The PDF file.", blank=True, null=True)
