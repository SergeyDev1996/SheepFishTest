import io
import os
import zipfile

from django.conf import settings
from django.http import FileResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from checks.models import Check
from printer.models import Printer
from .serializers import CheckSerializer
from .tasks import generate_pdf_receipt_task


class GenerateChecksView(CreateAPIView):
    serializer_class = CheckSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        printers = Printer.objects.filter(point_id=serializer.data["point_id"])
        if not printers:
            raise ValidationError("There are no printers for this point.")
        order = serializer.data["order"]
        check_exist = Check.objects.filter(order=order).first()
        if check_exist:
            raise ValidationError("The check for this order already exists.")
        for printer in printers:
            check = Check(
                printer_id=printer,
                type=serializer.data["type"],
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
        api_key = request.data.get("api_key")
        if not api_key:
            raise ValidationError("Please specify the api_key")
        printer = Printer.objects.filter(api_key=api_key).first()
        if not printer:
            raise ValidationError("Printer with this API key does not exist.")
        checks = Check.objects.filter(printer_id=printer,
                                      status=Check.CheckStatusChoices.RENDERED,
                                      printer_id__check_type=printer.
                                      check_type)
        if not checks:
            raise ValidationError("This printer does not"
                                  " have any new checks.")
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as archive:
            for check in checks:
                pdf_path = os.path.join(settings.MEDIA_ROOT,
                                        str(check.pdf_file))
                if os.path.exists(pdf_path):
                    archive.write(pdf_path, os.path.basename(pdf_path))
                check.status = Check.CheckStatusChoices.PRINTED
                check.save()
        # Set the file pointer to the beginning
        zip_buffer.seek(0)
        # Return the zip file as a response
        response = FileResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition']\
            = 'attachment; filename=rendered_checks.zip'
        return response
