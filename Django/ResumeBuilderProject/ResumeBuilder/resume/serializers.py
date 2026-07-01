from rest_framework import serializers
from .models import Employee, TechnicalSkill, Project, Responsibility,EmployeeProject




class TechnicalSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = TechnicalSkill
        fields = [
            "category",
            "skill",
        ]

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "project_name",
            "technology",
            "description",

        ]

class ResponsibilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Responsibility
        fields = [
            "responsibility",
        ]

class EmployeeProjectSerializer(serializers.ModelSerializer):

    project = ProjectSerializer(read_only=True)

    responsibilities = ResponsibilitySerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = EmployeeProject

        fields = [
            "project",
            "role",
            "responsibilities",
        ]

class EmployeeSerializer(serializers.ModelSerializer):

    skills = TechnicalSkillSerializer(
        many=True,
        read_only=True
    )

    projects = EmployeeProjectSerializer(
        source="employee_projects",
        many=True,
        read_only=True
    )

    class Meta:
        model = Employee

        fields = [
            "employee_id",
            "first_name",
            "last_name",
            "designation",
            "experience",
            "email",
            "phone",
            "summary",
            "skills",
            "projects",
        ]
