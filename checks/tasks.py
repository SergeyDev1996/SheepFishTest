from celery import shared_task

from checks.utils import generate_pdf_receipt


@shared_task
def generate_pdf_receipt_task(check_id):
    print("The lag is at the celery task")
    generate_pdf_receipt(check_id)
