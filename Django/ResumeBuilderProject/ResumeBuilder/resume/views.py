from django.shortcuts import render

from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from django.shortcuts import get_object_or_404

from .models import Employee
from .serializers import EmployeeSerializer
from django.http import FileResponse
from .pdf_generator import generate_resume
from django.views.generic import TemplateView


class SearchPageView(TemplateView):
    template_name = "resume/search.html"

class EmployeeSearchView(ListAPIView):
        serializer_class = EmployeeSerializer

        def get_queryset(self):
            search = self.request.query_params.get("search")

            if search:
             return Employee.objects.filter(
              Q(employee_id__icontains=search) |
              Q(first_name__icontains=search) |
              Q(last_name__icontains=search)
            )

            return Employee.objects.all()


class ResumeAPIView(RetrieveAPIView):

    serializer_class = EmployeeSerializer

    def get_object(self):

        employee_id = self.kwargs.get("employee_id")

        return get_object_or_404(
            Employee,
            employee_id=employee_id
        )
    
class ResumePDFView(RetrieveAPIView):

    def get(self, request, employee_id):

        employee = get_object_or_404(
            Employee,
            employee_id=employee_id
        )

        pdf = generate_resume(employee)

        return FileResponse(
            pdf,
            as_attachment=True,
            filename=f"{employee.employee_id}_Resume.pdf"
        )