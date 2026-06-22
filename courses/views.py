from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, CourseContent
from .serializers import CourseSerializer, CourseContentSerializer


class CourseListCreateView(APIView):

    def get(self, request):

        courses = Course.objects.all()

        serializer = CourseSerializer(
            courses,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = CourseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    def delete(self, request, pk):

        try:
            course = Course.objects.get(pk=pk)

            course.delete()

            return Response(
                {"message": "Course deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )

        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class CourseDetailView(APIView):

    def get(self, request, pk):

        try:
            course = Course.objects.get(pk=pk)

            serializer = CourseSerializer(course)

            return Response(serializer.data)

        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):

        try:
            course = Course.objects.get(pk=pk)

        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CourseSerializer(
            course,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        try:
            course = Course.objects.get(pk=pk)

            course.delete()

            return Response(
                {"message": "Course deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )

        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found"},
                status=status.HTTP_404_NOT_FOUND
            )
class CourseContentListCreateView(APIView):

    def get(self, request):

        contents = CourseContent.objects.all()

        serializer = CourseContentSerializer(
            contents,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = CourseContentSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class CourseContentDetailView(APIView):

    def get(self, request, pk):

        try:
            content = CourseContent.objects.get(pk=pk)

            serializer = CourseContentSerializer(content)

            return Response(serializer.data)

        except CourseContent.DoesNotExist:

            return Response(
                {"error": "Content not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):

        try:
            content = CourseContent.objects.get(pk=pk)

        except CourseContent.DoesNotExist:

            return Response(
                {"error": "Content not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CourseContentSerializer(
            content,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        try:
            content = CourseContent.objects.get(pk=pk)

            content.delete()

            return Response(
                {"message": "Content deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )

        except CourseContent.DoesNotExist:

            return Response(
                {"error": "Content not found"},
                status=status.HTTP_404_NOT_FOUND
            )       
