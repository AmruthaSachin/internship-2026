from rest_framework import serializers
from .models import Course, CourseContent


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class CourseContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseContent
        fields = '__all__'