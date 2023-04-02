from celery import shared_task
from .models import Check
from .utils import generate_pdf_receipt


@shared_task
def generate_pdf_receipt_task(check_id):
    return generate_pdf_receipt(check_id)
