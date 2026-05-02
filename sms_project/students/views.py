from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from students.forms import StudentForm
from students.models import Course, Profile, Student
from students.serializers import StudentSerializer


def home(request):
    total_courses = Course.objects.count()
    if request.user.is_authenticated:
        total_students = Student.objects.filter(created_by=request.user).count()
    else:
        total_students = 0
        
    return render(
        request,
        "home.html",
        {
            "total_students": total_students,
            "total_courses": total_courses,
        },
    )


@login_required
def dashboard(request):
    return render(
        request,
        "dashboard.html",
        {
            "total_students": Student.objects.filter(created_by=request.user).count(),
            "total_courses": Course.objects.count(),
            "user": request.user,
        },
    )


def register_user(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = UserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            messages.success(request, "Registration successful. Please login.")
            return redirect("login")
        messages.error(request, "Please fix the form errors and try again.")

    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Login successful.")
            return redirect("dashboard")
        messages.error(request, "Invalid username or password.")

    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


@login_required
def add_course(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if not name:
            messages.error(request, "Course name is required.")
            return redirect("add_course")
        if Course.objects.filter(name__iexact=name).exists():
            messages.warning(request, "This course already exists.")
            return redirect("add_course")

        Course.objects.create(name=name)
        messages.success(request, "Course added successfully.")
        return redirect("add_course")

    return render(
        request,
        "add_course.html",
        {"courses": Course.objects.all().order_by("name")},
    )


class StudentListView(ListView):
    model = Student
    template_name = "student_list.html"
    context_object_name = "students"
    paginate_by = 5

    def get_queryset(self):
        search_query = self.request.GET.get("search")
        sort_query = self.request.GET.get("sort", "id")
        allowed_sort = {
            "id": "id",
            "name": "name",
            "-name": "-name",
            "age": "age",
            "-age": "-age",
        }
        sort_by = allowed_sort.get(sort_query, "id")
        queryset = Student.objects.select_related("course").all()
        
        if self.request.user.is_authenticated:
            queryset = queryset.filter(created_by=self.request.user)
        else:
            queryset = queryset.none()
            
        queryset = queryset.order_by(sort_by)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(email__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_sort"] = self.request.GET.get("sort", "id")
        return context


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = "student_form.html"
    success_url = reverse_lazy("student_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Add Student"
        context["submit_label"] = "Save Student"
        context["form_subtitle"] = "Fill student details to add a new record."
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Student added successfully.")
        return super().form_valid(form)


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "student_form.html"
    success_url = reverse_lazy("student_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit Student"
        context["submit_label"] = "Update Student"
        context["form_subtitle"] = "Update student information and save changes."
        return context

    def form_valid(self, form):
        messages.success(self.request, "Student updated successfully.")
        return super().form_valid(form)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("student_list")

    def form_valid(self, form):
        messages.success(self.request, "Student deleted successfully.")
        return super().form_valid(form)


@api_view(["GET", "POST"])
def student_list(request):
    if request.method == "GET":
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(["GET", "PUT", "DELETE"])
def student_detail(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"})

    if request.method == "GET":
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    student.delete()
    return Response({"message": "Student deleted"})


# ============================================================================
# VIEWSETS AND ROUTERS - Advanced API Pattern (Day 20)
# ============================================================================

class StudentViewSet(ModelViewSet):
    """
    ViewSet for Student model - Combines all CRUD operations in one class.
    
    Automatically handles:
    - LIST: GET /api/v1/students/ 
    - CREATE: POST /api/v1/students/
    - RETRIEVE: GET /api/v1/students/{id}/
    - UPDATE: PUT /api/v1/students/{id}/
    - PARTIAL_UPDATE: PATCH /api/v1/students/{id}/
    - DESTROY: DELETE /api/v1/students/{id}/
    
    One ViewSet replaces 6 separate function-based views!
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        """Automatically set created_by to the current user"""
        serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        """
        Optional: Override to add custom filtering/searching
        Example: Filter by age, name search, etc.
        """
        queryset = Student.objects.select_related('course')
        
        if self.request.user.is_authenticated:
            queryset = queryset.filter(created_by=self.request.user)
        else:
            queryset = queryset.none()
        
        # Search by name or email (optional)
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(email__icontains=search_query)
            )
        
        # Sort by field (optional)
        sort_by = self.request.query_params.get('sort', None)
        if sort_by:
            queryset = queryset.order_by(sort_by)
        
        return queryset
