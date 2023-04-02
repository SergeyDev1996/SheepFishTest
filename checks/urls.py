from django.urls import path

from checks.views import GenerateChecksView, NewChecksView

urlpatterns = [
    path("check-generate/", GenerateChecksView.as_view(),
         name="check_generate"),
    path("print-checks/", NewChecksView.as_view(), name="new_checks")
]
