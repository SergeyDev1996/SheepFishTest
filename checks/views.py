import asyncio

from django.shortcuts import render
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from checks.models import Check
from checks.serializers import CheckCreateSerializer
from checks.utils import generate_pdf_receipt
from printer.models import Printer


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
        # check_exist = Check.objects.filter(order=order).first()
        # if check_exist:
        #     raise ValidationError("The check for this order already exists.")
        tasks = []
        for printer in printers:
            check = Check(
                printer_id=printer,
                type=request.data.get("type"),
                order=order,
                status=Check.CheckStatusChoices.NEW
            )
            check.save()
            generate_pdf_receipt(check.id)
        return Response({"success": "Order created and PDF generation started"}, status=status.HTTP_201_CREATED)
