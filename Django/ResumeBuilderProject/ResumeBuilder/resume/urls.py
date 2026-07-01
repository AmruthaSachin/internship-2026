from django.urls import path
from .views import (
    EmployeeSearchView,
    ResumeAPIView,
    ResumePDFView,
    SearchPageView,
)

urlpatterns = [
    path("", SearchPageView.as_view(), name="search-page"),

    path("employees/", EmployeeSearchView.as_view(), name="employee-search"),

    path("resume/<str:employee_id>/", ResumeAPIView.as_view(), name="resume"),

    path(
        "resume/<str:employee_id>/download/",
        ResumePDFView.as_view(),
        name="resume-download",
    ),
]