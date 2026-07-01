from rest_framework import serializers
from .models import Course, CourseContent, Enrollment
from accounts.models import CustomUser



class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = [
              'id',
              'title',
              'description',
              'price',
              'created_at'
               ]


class CourseContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseContent
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']