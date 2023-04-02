from django.contrib import admin

from checks.models import Check


@admin.register(Check)
class CheckAdmin(admin.ModelAdmin):
    list_filter = ("type", "printer_id", "status")
