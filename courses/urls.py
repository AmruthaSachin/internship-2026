from django.urls import path
from .views import CourseListCreateView, CourseDetailView, CourseContentListCreateView, CourseContentDetailView

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='courses'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('contents/', CourseContentListCreateView.as_view(), name = 'course-content'),
    path('contents/<int:pk>/', CourseContentDetailView.as_view(), name = 'course-content-detail'),

]
