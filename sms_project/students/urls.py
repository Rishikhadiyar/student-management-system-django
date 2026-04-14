from django.urls import path
from . import views
from .views import student_list

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.StudentCreateView.as_view(), name='create_student'),
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('delete/<int:pk>/', views.StudentDeleteView.as_view(), name='delete_student'),
    path('edit/<int:pk>/', views.StudentUpdateView.as_view(), name='edit_student'),
    path('students-api/', student_list),
]