from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import CustomUser
from .models import Course, CourseContent
from .serializers import CourseSerializer, CourseContentSerializer, StudentSerializer
from .models import Course, CourseContent, Enrollment
from .serializers import (
    CourseSerializer,
    CourseContentSerializer,
    EnrollmentSerializer
)
from django.core.mail import send_mail
import paypalrestsdk

from django.conf import settings

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

from rest_framework.views import APIView
from rest_framework.response import Response
import paypalrestsdk

class PurchasedStudentsView(APIView):

    def get(self, request, course_id):

        try:
            course = Course.objects.get(id=course_id)

        except Course.DoesNotExist:

            return Response(
                {"message": "Course not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Optional: only the course owner can see the students
        '''
        if course.teacher != request.user:

            return Response(
                {"message": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )
        '''

        enrollments = Enrollment.objects.filter(course=course)

        students = [
            enrollment.student
            for enrollment in enrollments
        ]

        serializer = StudentSerializer(
            students,
            many=True
        )

        return Response(serializer.data)


class CreatePaymentView(APIView):

    def post(self, request):

        payment = paypalrestsdk.Payment({

            "intent": "sale",

            "payer": {
                "payment_method": "paypal"
            },

            "redirect_urls": {
                "return_url": "http://127.0.0.1:8000/api/payment-success/",
                "cancel_url": "http://127.0.0.1:8000/api/payment-cancel/"
            },

            "transactions": [{
                "amount": {
                    "total": "10.00",
                    "currency": "USD"
                },
                "description": "Course Purchase"
            }]
        })

        if payment.create():

            for link in payment.links:

                if link.rel == "approval_url":

                    return Response({
                        "approval_url": link.href
                    })

        return Response(
            {"error": payment.error},
            status=400
        )
    
class PaymentSuccessView(APIView):

    def get(self, request):

        return Response({
            "message": "Payment Successful"
        })


class PaymentCancelView(APIView):

    def get(self, request):

        return Response({
            "message": "Payment Cancelled"
        })


class CourseListCreateView(APIView):

    #permission_classes = [IsTeacher]
    def get(self, request):

        search = request.GET.get('search')

        if search:
          courses = Course.objects.filter(
            title__icontains=search
          )
        else:
           courses = Course.objects.all()

        serializer = CourseSerializer(
        courses,
        many=True
        )

        return Response(serializer.data)

    def post(self, request):

       serializer = CourseSerializer(data=request.data)

       if serializer.is_valid():
        teacher = CustomUser.objects.get(id=1)


        course = serializer.save(
            teacher=teacher
        )

        send_mail(
            subject="Course Created Successfully",
            message=f"Hello {course.teacher.username},\n\nYour course '{course.title}' has been created successfully.\n\nThank you for using the Online Learning Platform!",
            from_email=None,
            recipient_list=[course.teacher.email],
            fail_silently=False,
        )

        students = CustomUser.objects.filter(
          enrollments__course__teacher=teacher
          ).distinct()

       for student in students:

        send_mail(
        subject="New Course Available",
        message=f"""
Hello {student.username},

Your instructor {teacher.username} has published a new course.

Course Name: {course.title}

Course Description:
{course.description}

Price: ${course.price}

Login to the Online Learning Platform to explore it.

Thank you.
""",
        from_email=None,
        recipient_list=[student.email],
        fail_silently=False,
    )

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
    def get(self, request, course_id):

       try:
        course = Course.objects.get(id=course_id)

       except Course.DoesNotExist:

          return Response(
            {"message": "Course not found"},
              status=status.HTTP_404_NOT_FOUND
           )

    # Temporary for testing
       student = CustomUser.objects.get(id=2)

       if not Enrollment.objects.filter(
        student=student,
        course=course
       ).exists():

           return Response(
            {"message": "Purchase the course first"},
            status=status.HTTP_403_FORBIDDEN
           )

       contents = CourseContent.objects.filter(course=course)

       serializer = CourseContentSerializer(
        contents,
        many=True
       )

       return Response(serializer.data)

    def post(self, request, course_id):
        serializer = CourseContentSerializer(
        data=request.data
        )

        if serializer.is_valid():

           course = Course.objects.get(id=course_id)

           content = serializer.save(course=course)

           enrollments = Enrollment.objects.filter(
            course=course
           )

           for enrollment in enrollments:

               send_mail(
               subject="New Topic Added",
               message=f"""
            Hello {enrollment.student.username},

            A new topic '{content.title}' has been added to the course'{content.course.title}'.

            Login to continue learning.

            Thank you.
            """,
                from_email=None,
                recipient_list=[enrollment.student.email],
                fail_silently=False,
                )

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

class EnrollmentListCreateView(APIView):

    def get(self, request):

        enrollments = Enrollment.objects.all()

        serializer = EnrollmentSerializer(
            enrollments,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = EnrollmentSerializer(
            data=request.data
        )

        if serializer.is_valid():

            enrollment = serializer.save()

            send_mail(
             subject="Enrollment Successful",
             message=f"You have successfully enrolled in {enrollment.course.title}. Happy Learning!",
             from_email=None,
             recipient_list=[enrollment.student.email],
             fail_silently=False,
            )

            return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )