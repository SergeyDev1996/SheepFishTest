from django.db import models


class Printer(models.Model):
    class PrintCheckType(models.TextChoices):
        KITCHEN = 'Kitchen'
        CLIENT = 'Client'
    name = models.CharField(max_length=50, help_text="The printer name.")
    api_key = models.CharField(max_length=255, help_text="The API access key.")
    check_type = models.CharField(max_length=50, choices=PrintCheckType.choices, help_text="The check type.")
    point_id = models.IntegerField(help_text="The point to which the printer is connected to.")


class Check(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('error', 'Error'),
    ]
    TYPE_CHOICES = [
        ('client', 'Client'),
        ('kitchen', 'Kitchen'),
    ]
    order_id = models.IntegerField(unique=True)
    printer = models.ForeignKey(Printer, on_delete=models.CASCADE)
    check_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    pdf_file = models.FileField(upload_to='pdf/', blank=True, null=True)
