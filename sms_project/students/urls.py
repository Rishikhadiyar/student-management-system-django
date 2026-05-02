from django.urls import path
from students import views
from students.views import student_list

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('courses/add/', views.add_course, name='add_course'),
    path('create/', views.StudentCreateView.as_view(), name='create_student'),
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('delete/<int:pk>/', views.StudentDeleteView.as_view(), name='delete_student'),
    path('edit/<int:pk>/', views.StudentUpdateView.as_view(), name='edit_student'),
    path('students-api/', student_list),
]
