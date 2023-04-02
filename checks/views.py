import asyncio
import io
import os
import zipfile

from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from checks.models import Check
from checks.serializers import CheckCreateSerializer
from printer.models import Printer
from .tasks import generate_pdf_receipt_task


class GenerateChecksView(CreateAPIView):
    serializer_class = CheckCreateSerializer

    def post(self, request, *args, **kwargs):
        point_id = request.data.get("point_id")
        if not point_id:
            raise ValidationError("Please specify point id.")
        printers = Printer.objects.filter(point_id=request.data.get("point_id"))
        if not printers:
            raise ValidationError("There are no printers for this point.")
        order = request.data.get("order")
        check_exist = Check.objects.filter(order=order).first()
        # if check_exist:
        #     raise ValidationError("The check for this order already exists.")
        for printer in printers:
            check = Check(
                printer_id=printer,
                type=request.data.get("type"),
                order=order,
                status=Check.CheckStatusChoices.NEW,
            )
            check.save()
            generate_pdf_receipt_task.delay(check.id)
        return Response(
            {"success": "Order created and PDF generation started"},
            status=status.HTTP_201_CREATED,
        )


class NewChecksView(APIView):

    def post(self, request, *args, **kwargs):
        printer = Printer.objects.filter(id=request.data.get("printer_id")).first()
        if not printer:
            raise ValidationError("Please specify the printer id.")
        checks = Check.objects.filter(printer_id=printer, status=Check.CheckStatusChoices.RENDERED)
        if not checks:
            raise ValidationError("This printer does not have any new checks.")
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as archive:
            for check in checks:
                pdf_path = os.path.join(settings.MEDIA_ROOT, str(check.pdf_file))
                if os.path.exists(pdf_path):
                    print(f"Adding PDF file to archive: {pdf_path}")  # Add this line to debug
                    archive.write(pdf_path, os.path.basename(pdf_path))
                else:
                    print(f"PDF file not found: {pdf_path}")  # Add this line to debug
        # Set the file pointer to the beginning
        zip_buffer.seek(0)
        # Return the zip file as a response
        response = FileResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=rendered_checks.zip'
        return response

