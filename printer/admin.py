from django.contrib import admin

from printer.models import Printer


@admin.register(Printer)
class PrinterAdmin(admin.ModelAdmin):
    pass
