from django.contrib import admin
from .models import (
    Employee,
    TechnicalSkill,
    Project,
    EmployeeProject,
    Responsibility
)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "employee_id",
        "first_name",
        "last_name",
        "designation",
        "experience",
    )

    search_fields = (
        "employee_id",
        "first_name",
        "last_name",
    )


@admin.register(TechnicalSkill)
class TechnicalSkillAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "category",
        "skill",
    )

    search_fields = (
        "employee__employee_id",
        "employee__first_name",
        "skill",
    )

    list_filter = (
        "category",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "project_name",
        "technology",
    )

    search_fields = (
        "project_name",
    )


@admin.register(EmployeeProject)
class EmployeeProjectAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "project",
        "role",
    )

    search_fields = (
        "employee__employee_id",
        "employee__first_name",
        "project__project_name",
    )


@admin.register(Responsibility)
class ResponsibilityAdmin(admin.ModelAdmin):
    list_display = (
        "employee_project",
        "responsibility",
    )

    search_fields = (
        "employee_project__employee__employee_id",
        "employee_project__project__project_name",
    )