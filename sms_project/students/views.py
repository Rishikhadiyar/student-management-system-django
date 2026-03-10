from urllib import request

from django.shortcuts import render,redirect
from .models import Student
from django.contrib import messages
from django.core.paginator import Paginator

def home(request):
   total_students = Student.objects.count()

   return render(request,'home.html',{
        'total_students': total_students
    })


def create_student(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        age = request.POST['age']
        course = request.POST['course']

        Student.objects.create(
            name=name,
            email=email,
            age=age,
            course=course
        )
        messages.success(request,"Student Added Successfully")

        return redirect('student_list')

    return render(request, 'create_student.html')

def student_list(request):

    search_query = request.GET.get('search','')

    if search_query:
        student_list = Student.objects.filter(name__icontains=search_query)
    else:
        student_list = Student.objects.all()

    paginator = Paginator(student_list,5)

    page_number = request.GET.get('page')

    students = paginator.get_page(page_number)

    return render(request,'student_list.html',{
        'students':students,
        'search_query':search_query
    })


def delete_student(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    messages.success(request,"Student Deleted Successfully")
    return redirect('student_list')
# Create your views here.
def edit_student(request, id):

    student = Student.objects.get(id=id)

    if request.method == "POST":
        student.name = request.POST['name']
        student.email = request.POST['email']
        student.age = request.POST['age']
        student.course = request.POST['course']

        student.save()
        messages.success(request,"Student Updated Successfully")
        return redirect('student_list')

    return render(request, 'edit_student.html', {'student': student})