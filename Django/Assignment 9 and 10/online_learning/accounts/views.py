from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.http import HttpResponse

import random

from django.core.mail import send_mail
from .models import EmailOTP

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    EmailOTPSerializer,
    VerifyOTPSerializer
)



class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            send_mail(
              subject="Registration Successful",
              message=f"Hello {user.username},\n\nWelcome to the Online Learning Platform! Your account has been created successfully.",
              from_email=None,
              recipient_list=[user.email],
              fail_silently=False,
            )

            return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(
                request,
                username=email,
                password=password
            )

            if user:
                return Response(
                    {
                        "message": "Login successful",
                        "role": user.role
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    



def test_email(request):

    send_mail(
        subject='Django Test Email',
        message='Congratulations! Your email configuration is working.',
        from_email=None,
        recipient_list=['amrutha.nagvekar@gmail.com'],
        fail_silently=False,
    )

    return HttpResponse("Email sent successfully!")

class SendOTPView(APIView):

    def post(self, request):

        serializer = EmailOTPSerializer(data=request.data)

        if serializer.is_valid():

            email = serializer.validated_data['email']

            otp = str(random.randint(100000, 999999))

            EmailOTP.objects.create(
                email=email,
                otp=otp
            )

            send_mail(
                subject="Your OTP",
                message=f"Your OTP is {otp}",
                from_email=None,
                recipient_list=[email],
                fail_silently=False,
            )

            return Response(
                {"message": "OTP sent successfully"}
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class VerifyOTPView(APIView):

    def post(self, request):

        serializer = VerifyOTPSerializer(data=request.data)

        if serializer.is_valid():

            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']

            try:
                otp_obj = EmailOTP.objects.get(
                    email=email,
                    otp=otp
                )

                otp_obj.delete()


                return Response(
                    {"message": "OTP verified successfully"}
                )

            except EmailOTP.DoesNotExist:

                return Response(
                    {"message": "Invalid OTP"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )