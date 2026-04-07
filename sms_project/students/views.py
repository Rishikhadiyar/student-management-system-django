from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q
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

class StudentListView(ListView):
    model = Student
    template_name = 'student_list.html'
    context_object_name = 'students'
    paginate_by = 5

    def get_queryset(self):
        search_query = self.request.GET.get('search')

        if search_query:
            return Student.objects.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        return Student.objects.all()