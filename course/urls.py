from django.urls import path
from .views import CourseListCreateView, CourseDetailView

app_name = 'course'

urlpatterns = [
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
]
