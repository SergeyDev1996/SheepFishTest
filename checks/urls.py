from django.urls import path

from checks.views import GenerateChecksView

urlpatterns = [
    path("check-generate/", GenerateChecksView.as_view(), name="check_generate")
]
