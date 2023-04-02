import base64
import json
import os

import httpx
from channels.db import database_sync_to_async
from django.conf import settings
import requests

from checks.models import Check


def generate_pdf_receipt(check_id: int):
    check = Check.objects.get(id=check_id)
    url = "http://wkhtmltopdf:80/"
    with open("templates/check.html", "rb") as f:
        file_contents = f.read()
    encoded_contents = base64.b64encode(file_contents).decode("utf-8")
    data = {
        'contents': encoded_contents,
    }
    headers = {
        'Content-Type': 'application/json',  # This is important
    }
    response = requests.post(url=url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        pdf_dir = os.path.join(settings.MEDIA_ROOT, 'pdf')
        os.makedirs(pdf_dir, exist_ok=True)
        file_path = os.path.join(pdf_dir, f'{check.id}.pdf')
        with open(file_path, 'wb+') as f:
            f.write(response.content)
        check.pdf_file = f'receipts/{check.id}.pdf'
        check.save()
