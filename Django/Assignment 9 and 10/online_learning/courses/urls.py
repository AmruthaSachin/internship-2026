from django.urls import path
from .views import CourseListCreateView, CourseDetailView, CourseContentListCreateView, CourseContentDetailView, EnrollmentListCreateView,CreatePaymentView,PaymentSuccessView,PaymentCancelView, PurchasedStudentsView

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='courses'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path("courses/<int:course_id>/contents/",CourseContentListCreateView.as_view(),name="course-content"),
    path('contents/<int:pk>/', CourseContentDetailView.as_view(), name = 'course-content-detail'),
    path('enrollments/',EnrollmentListCreateView.as_view(),name='enrollments'),
    path("create-payment/",CreatePaymentView.as_view(),name="create-payment"),
    path("payment-success/",PaymentSuccessView.as_view(),name="payment-success"),
    path("payment-cancel/",PaymentCancelView.as_view(),name="payment-cancel"),
    path("courses/<int:course_id>/students/",PurchasedStudentsView.as_view(),name="purchased-students"),


]
