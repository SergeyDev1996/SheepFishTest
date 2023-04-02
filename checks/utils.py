import base64
import json
import os

from django.conf import settings
import requests
from django.template.loader import get_template

from checks.models import Check


def generate_pdf_receipt(check_id: int) -> None:
    check = Check.objects.get(id=check_id)
    url = f"http://{os.environ.get('HTMLTOPDFHOST')}:" \
          f"{os.environ.get('HTMLTOPDFPORT')}/"
    context = {"check_type": check.type,
               "check_id": check.id}
    template = get_template("check.html")
    html = template.render(context=context)
    encoded_contents = base64.b64encode(html.encode("utf-8")).decode("utf-8")
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
        check.save()
