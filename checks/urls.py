from django.urls import path

from checks.views import GenerateChecksView, NewChecksView

urlpatterns = [
    path("check-generate/", GenerateChecksView.as_view(), name="check_generate"),
    path("new-checks/", NewChecksView.as_view(), name="new_checks")
]
