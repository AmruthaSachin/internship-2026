from django.shortcuts import render

from django.db.models import Q
from rest_framework.generics import ListAPIView

from .models import Employee
from .serializers import EmployeeSerializer

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
