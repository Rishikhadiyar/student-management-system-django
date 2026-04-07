from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.db.models import Q
from .models import Student
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic import DeleteView

def home(request):
   total_students = Student.objects.count()

   return render(request,'home.html',{
        'total_students': total_students
    })







# Create your views here.

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
    
class StudentCreateView(CreateView):
    model = Student
    fields = ['name', 'email', 'age', 'course']
    template_name = 'create_student.html'
    success_url = reverse_lazy('student_list')   
    
class StudentUpdateView(UpdateView):
    model = Student
    fields = ['name', 'email', 'age', 'course']
    template_name = 'edit_student.html'
    success_url = reverse_lazy('student_list')     
    
    
class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('student_list')    