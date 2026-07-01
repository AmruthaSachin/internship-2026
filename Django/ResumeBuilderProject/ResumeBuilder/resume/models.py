from django.db import models

class Employee(models.Model):
    employee_id = models.CharField(max_length = 20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    designation = models.CharField(max_length=100)
    experience = models.DecimalField(max_digits=4, decimal_places=1)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    summary = models.TextField()

    def __str__(self):
        return f"{self.employee_id} - {self.first_name} {self.last_name}"
    
class TechnicalSkill(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    category = models.CharField(max_length=100)
    skill = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category} - {self.skill}"


class Project(models.Model):
    project_name = models.CharField(max_length=100)
    technology = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.project_name
    
class EmployeeProject(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="employee_projects"
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="project_employees"
    )
    role = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.employee.first_name} - {self.project.project_name}"

class Responsibility(models.Model):
    employee_project = models.ForeignKey(
        EmployeeProject,
        on_delete=models.CASCADE,
        related_name="responsibilities"
    )

    responsibility = models.TextField()

    def __str__(self):
        return self.responsibility



