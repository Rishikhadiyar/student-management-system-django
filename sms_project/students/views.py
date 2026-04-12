from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from .models import Student
from django.contrib import messages
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
        queryset = Student.objects.all().order_by('id')

        if search_query:
            return queryset.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        return queryset
    
class StudentCreateView(CreateView):
    model = Student
    fields = ['name', 'email', 'age', 'course']
    template_name = 'create_student.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        messages.success(self.request, 'Student added successfully.')
        return super().form_valid(form)
    
class StudentUpdateView(UpdateView):
    model = Student
    fields = ['name', 'email', 'age', 'course']
    template_name = 'edit_student.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        messages.success(self.request, 'Student updated successfully.')
        return super().form_valid(form)
    
    
class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        messages.success(self.request, 'Student deleted successfully.')
        return super().form_valid(form)
