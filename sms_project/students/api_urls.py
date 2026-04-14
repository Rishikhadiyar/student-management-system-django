from django.urls import path
from .views import student_list, student_detail

urlpatterns = [
    path('students-api/', student_list),
    path('students-api/<int:pk>/', student_detail),
]