import base64
import json
import os

from django.conf import settings
import requests

from checks.models import Check


def generate_pdf_receipt(check_id: int) -> None:
    check = Check.objects.get(id=check_id)
    url = "http://wkhtmltopdf:80/"
    with open("templates/check.html", "rb") as f:
        file_contents = f.read()
    encoded_contents = base64.b64encode(file_contents).decode("utf-8")
    data = {
        "contents": encoded_contents,
    }
    headers = {
        "Content-Type": "application/json",
    }
    order_id = check.order["order_id"]
    response = requests.post(url=url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        pdf_dir = os.path.join(settings.MEDIA_ROOT, "pdf")
        os.makedirs(pdf_dir, exist_ok=True)
        file_path = os.path.join(pdf_dir, f"{order_id}_{check.type}.pdf")
        with open(file_path, "wb+") as f:
            f.write(response.content)
        check.pdf_file = os.path.join("pdf", f"{order_id}_{check.type}.pdf")
        check.status = Check.CheckStatusChoices.RENDERED
        print(f"Updating check {check.id} status to RENDERED")  # Add this line to debug
        check.save()
        print(f"Check {check.id} status updated to RENDERED")  # Add this line to debug
    else:
        print(f"PDF generation failed for check {check.id} with status code {response.status_code}")  # Add this line to debug
