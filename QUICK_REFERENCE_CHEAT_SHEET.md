# 📋 Django Advanced Topics - Quick Reference Cheat Sheet

## ORM Query Patterns

### Basic Operations
```python
# Fetch all
Student.objects.all()

# Count
Student.objects.count()

# First & Last
Student.objects.first()
Student.objects.last()

# Exists
Student.objects.filter(name="Rahul").exists()
```

### Filter Operations
```python
# Exact match
Student.objects.filter(name="Rahul")

# Greater than
Student.objects.filter(age__gt=20)

# Greater than or equal
Student.objects.filter(age__gte=20)

# Less than
Student.objects.filter(age__lt=20)

# Less than or equal
Student.objects.filter(age__lte=20)

# Contains (case-sensitive)
Student.objects.filter(name__contains="rah")

# Contains (case-insensitive)
Student.objects.filter(name__icontains="rah")

# Starts with
Student.objects.filter(name__startswith="R")

# Ends with
Student.objects.filter(email__endswith="@gmail.com")

# In list
Student.objects.filter(age__in=[20, 21, 22])

# Is null
Student.objects.filter(course__isnull=True)
```

### Exclude
```python
Student.objects.exclude(age=18)
Student.objects.exclude(name__icontains="test")
```

### Q Objects (Complex Queries)
```python
from django.db.models import Q

# OR
Q(age=20) | Q(name="Rahul")

# AND
Q(age=20) & Q(name="Rahul")

# NOT
~Q(age=18)

# Combined
(Q(age__gte=20) & Q(course_id=1)) | Q(name__icontains="ra")
```

### Ordering
```python
# Ascending
Student.objects.order_by("name")

# Descending
Student.objects.order_by("-age")

# Multiple fields
Student.objects.order_by("course", "-age")
```

### Get Single Object
```python
# Get by primary key
Student.objects.get(pk=1)
Student.objects.get(id=1)

# Get by field
Student.objects.get(email="user@example.com")

# With error handling
from django.shortcuts import get_object_or_404
student = get_object_or_404(Student, id=1)
```

### Performance
```python
# Select related (ForeignKey)
Student.objects.select_related('course')

# Prefetch related (ManyToMany, Reverse ForeignKey)
Post.objects.prefetch_related('tags')

# Only specific fields
Student.objects.only('name', 'email')

# Exclude specific fields
Student.objects.defer('bio')

# Distinct
Student.objects.distinct()
```

### Chaining
```python
students = Student.objects.all()
students = students.filter(age__gte=20)
students = students.filter(name__icontains="ra")
students = students.order_by("-age")
results = list(students)  # Execute query
```

---

## Class-Based Views Patterns

### ListView
```python
from django.views.generic import ListView

class StudentListView(ListView):
    model = Student
    template_name = "students.html"
    context_object_name = "students"
    paginate_by = 10
    
    def get_queryset(self):
        return Student.objects.order_by('-id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Student List"
        return context
```

### DetailView
```python
from django.views.generic import DetailView

class StudentDetailView(DetailView):
    model = Student
    template_name = "student_detail.html"
    context_object_name = "student"
    
    def get_queryset(self):
        return Student.objects.select_related('course')
```

### CreateView
```python
from django.views.generic import CreateView
from django.urls import reverse_lazy

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = "student_form.html"
    success_url = reverse_lazy("student_list")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Student added!")
        return response
```

### UpdateView
```python
from django.views.generic import UpdateView

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "student_form.html"
    success_url = reverse_lazy("student_list")
    
    def form_valid(self, form):
        messages.success(self.request, "Updated!")
        return super().form_valid(form)
```

### DeleteView
```python
from django.views.generic import DeleteView

class StudentDeleteView(DeleteView):
    model = Student
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("student_list")
```

---

## Template Patterns

### Pagination
```html
{% if page_obj.has_previous %}
    <a href="?page=1">First</a>
    <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
{% endif %}

Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}

{% if page_obj.has_next %}
    <a href="?page={{ page_obj.next_page_number }}">Next</a>
    <a href="?page={{ page_obj.paginator.num_pages }}">Last</a>
{% endif %}
```

### Search Form
```html
<form method="GET">
    <input type="text" name="search" placeholder="Search..." value="{{ request.GET.search }}">
    <button type="submit">Search</button>
</form>
```

### Maintain Search + Sort in Pagination
```html
<a href="?search={{ request.GET.search }}&sort={{ sort }}&page={{ next_page }}">
    Next
</a>
```

### For Loop with Empty
```html
{% for student in students %}
    <p>{{ student.name }} - {{ student.email }}</p>
{% empty %}
    <p>No students found</p>
{% endfor %}
```

---

## Serializers (API)

### Basic Serializer
```python
from rest_framework import serializers

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'  # All fields
        # fields = ['name', 'email', 'age']  # Specific fields
        # exclude = ['created_at']  # Exclude fields
        read_only_fields = ['id', 'created_at']
```

### Custom Serializer
```python
class StudentSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'age', 'course', 'course_name']
    
    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError("Age must be 18+")
        return value
```

---

## API Views Patterns

### Function-Based API Views
```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def student_list(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    if request.method == 'DELETE':
        student.delete()
        return Response(status=204)
```

### ViewSet (Class-Based API)
```python
from rest_framework.viewsets import ModelViewSet

class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def get_queryset(self):
        queryset = Student.objects.all()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(email__icontains=search)
            )
        return queryset
```

### Router (Auto URLs)
```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('students', StudentViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
```

---

## URL Patterns

### Web Views
```python
path('students/', StudentListView.as_view(), name='student_list'),
path('students/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
path('create/', StudentCreateView.as_view(), name='create_student'),
path('edit/<int:pk>/', StudentUpdateView.as_view(), name='edit_student'),
path('delete/<int:pk>/', StudentDeleteView.as_view(), name='delete_student'),
```

### API Endpoints (Function-Based)
```python
path('api/students/', student_list),
path('api/students/<int:pk>/', student_detail),
```

### API Endpoints (ViewSet + Router)
```python
router = DefaultRouter()
router.register('students', StudentViewSet)
path('api/v1/', include(router.urls)),
```

---

## Common HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | GET successful |
| 201 | Created | POST successful |
| 204 | No Content | DELETE successful |
| 400 | Bad Request | Invalid data |
| 401 | Unauthorized | Not authenticated |
| 403 | Forbidden | No permission |
| 404 | Not Found | Object doesn't exist |
| 500 | Server Error | Something broke |

---

## Testing in Django Shell

```bash
python manage.py shell
```

```python
from students.models import Student
from django.db.models import Q

# Create
student = Student.objects.create(
    name="John",
    email="john@example.com",
    age=20,
    course_id=1
)

# Read
student = Student.objects.get(id=1)
print(student.name)

# Update
student.name = "Jane"
student.save()

# Delete
student.delete()

# Query
students = Student.objects.filter(age__gte=20)
print(list(students))
```

---

## Best Practices ✅

1. **Use select_related() for ForeignKey**
   ```python
   Student.objects.select_related('course')
   ```

2. **Use prefetch_related() for ManyToMany**
   ```python
   Post.objects.prefetch_related('tags')
   ```

3. **Use get_object_or_404() instead of get()**
   ```python
   from django.shortcuts import get_object_or_404
   student = get_object_or_404(Student, id=1)
   ```

4. **Use Q objects for complex queries**
   ```python
   from django.db.models import Q
   Student.objects.filter(Q(age__gte=20) & Q(course_id=1))
   ```

5. **Always use many=True for multiple serializations**
   ```python
   StudentSerializer(students, many=True)
   ```

6. **Override get_queryset() instead of setting queryset**
   ```python
   def get_queryset(self):
       return Student.objects.select_related('course')
   ```

7. **Use reverse_lazy() for success_url**
   ```python
   success_url = reverse_lazy('student_list')
   ```

8. **Validate serializer data**
   ```python
   if serializer.is_valid():
       serializer.save()
   else:
       return Response(serializer.errors)
   ```

---

## Common Mistakes ❌

| Mistake | Issue | Solution |
|---------|-------|----------|
| Forgetting `many=True` | Serializer fails with multiple objects | `StudentSerializer(students, many=True)` |
| Using `.get()` without try-except | 404 errors crash | Use `get_object_or_404()` |
| N+1 query problem | Slow queries | Use `select_related()` |
| Forgetting `.as_view()` in URLs | CBV doesn't work | `StudentListView.as_view()` |
| Wrong context_object_name | Template variables empty | Match template variable name |
| Forgetting `data=request.data` | API POST fails | `StudentSerializer(data=request.data)` |
| Not calling `.save()` | Data not persisted | Always call `serializer.save()` |
| Using old API viewsin router | URLs conflict | Use ViewSet instead |

---

## Quick Command Reference

```bash
# Start development server
python manage.py runserver

# Enter Django shell
python manage.py shell

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Database reset
python manage.py flush
```

---

## 🎯 Quick Decision Tree

```
Need to show data?
├─ Yes, in UI → Use ListView
├─ Single item detail → Use DetailView
└─ No, API → Use ViewSet + Router

Need to modify data?
├─ Create → Use CreateView (UI) or ModelViewSet (API)
├─ Update → Use UpdateView (UI) or ModelViewSet (API)
└─ Delete → Use DeleteView (UI) or ModelViewSet (API)

Need to filter/search?
├─ Simple → Use .filter()
├─ Complex → Use Q objects
└─ In API → Override get_queryset()

Need pagination?
└─ In ListView: paginate_by = 10
└─ In API: DRF handles it automatically

Need sorting?
├─ In UI → Use order_by() in get_queryset()
└─ In API → Allow query parameter in get_queryset()
```

---

**All 12 Django Advanced Topics - Quick Reference Complete!** 📚
