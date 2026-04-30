# 🧪 Complete Testing & Usage Guide
# Django Advanced Topics - Practical Examples

## Part 1: Testing ORM Queries in Django Shell

### Enter Django Shell
```bash
cd sms_project
python manage.py shell
```

### Test 1: Fetch All Data
```python
from students.models import Student

# Get all students
students = Student.objects.all()
print(students)

# Get count
print(f"Total students: {students.count()}")
```

### Test 2: Filter Data
```python
# Single filter
rahul = Student.objects.filter(name="Rahul")
print(rahul)

# Multiple filters (AND condition)
students = Student.objects.filter(age=20, name="Rahul")
print(students)
```

### Test 3: Exclude Data
```python
# Get all except age 18
students = Student.objects.exclude(age=18)
print(students)
```

### Test 4: Get Single Object
```python
# Get by ID (pk)
student = Student.objects.get(pk=1)
print(student)
print(student.name, student.email)
```

### Test 5: Order Data (Sorting)
```python
# Sort A-Z
students = Student.objects.order_by("name")
for s in students:
    print(s.name)

# Sort Z-A
students = Student.objects.order_by("-name")
print(students)

# Sort by age (low to high)
students = Student.objects.order_by("age")
print(students)

# Sort by age (high to low)
students = Student.objects.order_by("-age")
print(students)
```

### Test 6: Search Using icontains
```python
# Case-insensitive search
students = Student.objects.filter(name__icontains="ra")
print(students)

# Search by email
students = Student.objects.filter(email__icontains="gmail")
print(students)
```

### Test 7: Using Q Objects (Complex Queries)
```python
from django.db.models import Q

# OR condition - name contains "ra" OR age is 20
students = Student.objects.filter(
    Q(name__icontains="ra") | Q(age=20)
)
print(students)

# AND condition - name contains "ra" AND age is 20
students = Student.objects.filter(
    Q(name__icontains="ra") & Q(age=20)
)
print(students)

# NOT condition
students = Student.objects.filter(~Q(age=18))
print(students)
```

### Test 8: Count & Exists
```python
# Count records
count = Student.objects.count()
print(f"Total: {count}")

# Check if exists
exists = Student.objects.filter(name="Rahul").exists()
print(f"Rahul exists: {exists}")

# Get count with filter
count = Student.objects.filter(age__gte=20).count()
print(f"Students 20+: {count}")
```

### Test 9: Chaining Queries
```python
# Start with all
queryset = Student.objects.all()

# Add filter
queryset = queryset.filter(age__gte=18)

# Add search
queryset = queryset.filter(name__icontains="ra")

# Add sorting
queryset = queryset.order_by("-age")

# Get results
print(queryset)
```

---

## Part 2: Testing Web Views (UI)

### Start Development Server
```bash
python manage.py runserver 127.0.0.1:8000
```

### Test 1: Student List with Search
```
URL: http://localhost:8000/students/
```
✅ Features:
- See all students
- Search by name or email
- Sort dropdown (Name A-Z, Z-A, Age High-Low)
- Pagination (5 per page)

### Test 2: Search Functionality
```
URL: http://localhost:8000/students/?search=rahul
URL: http://localhost:8000/students/?search=gmail
```
✅ Features:
- Search box works
- Results filtered
- Pagination maintained

### Test 3: Sorting
```
URL: http://localhost:8000/students/?sort=name
URL: http://localhost:8000/students/?sort=-name
URL: http://localhost:8000/students/?sort=age
URL: http://localhost:8000/students/?sort=-age
```
✅ Features:
- Dropdown changes sort
- Results reordered

### Test 4: Combined Search + Sort + Pagination
```
URL: http://localhost:8000/students/?search=rahul&sort=-age&page=2
```
✅ Features:
- Search active
- Sorting active
- Pagination works

### Test 5: Add Student (CreateView)
```
URL: http://localhost:8000/create/
```
✅ Actions:
1. Click "Add Student" button
2. Fill form
3. Submit
4. Redirects to list

### Test 6: Edit Student (UpdateView)
```
URL: http://localhost:8000/edit/1/
```
✅ Actions:
1. Click "Edit" button
2. Form prefilled with data
3. Modify fields
4. Submit
5. Redirects to list

### Test 7: Delete Student (DeleteView)
```
URL: http://localhost:8000/delete/1/
```
✅ Actions:
1. Click "Delete" button
2. Confirmation page shown
3. Click confirm
4. Student deleted
5. Redirects to list

---

## Part 3: Testing API Endpoints

### Install cURL or Use REST Client
- **Option 1**: cURL command line
- **Option 2**: Postman (GUI)
- **Option 3**: VS Code REST Client extension
- **Option 4**: Browser (for GET requests)

### Test 1: Get All Students (GET)
```bash
# cURL
curl http://localhost:8000/api/students-api/

# OR visit in browser
http://localhost:8000/api/students-api/
```

Response:
```json
[
  {
    "id": 1,
    "name": "Rahul",
    "email": "rahul@example.com",
    "age": 20,
    "course": 1,
    "profile_image": null
  }
]
```

### Test 2: Create New Student (POST)
```bash
curl -X POST http://localhost:8000/api/students-api/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Student",
    "email": "new@example.com",
    "age": 22,
    "course": 1
  }'
```

### Test 3: Get Single Student (GET)
```bash
curl http://localhost:8000/api/students-api/1/
```

Response:
```json
{
  "id": 1,
  "name": "Rahul",
  "email": "rahul@example.com",
  "age": 20,
  "course": 1
}
```

### Test 4: Update Student (PUT)
```bash
curl -X PUT http://localhost:8000/api/students-api/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rahul Updated",
    "email": "rahul_new@example.com",
    "age": 21,
    "course": 1
  }'
```

### Test 5: Delete Student (DELETE)
```bash
curl -X DELETE http://localhost:8000/api/students-api/1/
```

Response:
```json
{
  "message": "Student deleted"
}
```

---

## Part 4: Testing New ViewSet + Router Endpoints

### Test 1: List via ViewSet (GET)
```bash
curl http://localhost:8000/api/v1/students/
```

### Test 2: Create via ViewSet (POST)
```bash
curl -X POST http://localhost:8000/api/v1/students/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vikram",
    "email": "vikram@example.com",
    "age": 23,
    "course": 2
  }'
```

### Test 3: Retrieve via ViewSet (GET)
```bash
curl http://localhost:8000/api/v1/students/1/
```

### Test 4: Update via ViewSet (PUT)
```bash
curl -X PUT http://localhost:8000/api/v1/students/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Vikram Updated",
    "email": "vikram_new@example.com",
    "age": 24,
    "course": 2
  }'
```

### Test 5: Partial Update via ViewSet (PATCH)
```bash
curl -X PATCH http://localhost:8000/api/v1/students/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "age": 25
  }'
```

### Test 6: Delete via ViewSet (DELETE)
```bash
curl -X DELETE http://localhost:8000/api/v1/students/1/
```

### Test 7: Search via ViewSet
```bash
curl "http://localhost:8000/api/v1/students/?search=vikram&sort=name"
```

---

## Part 5: Using Postman (Recommended for Testing)

### Setup in Postman

1. **Create Collection**: "Student Management System"
2. **Add Requests**:

#### Request 1: Get All Students
```
Method: GET
URL: http://localhost:8000/api/v1/students/
```

#### Request 2: Create Student
```
Method: POST
URL: http://localhost:8000/api/v1/students/
Body (JSON):
{
  "name": "Priya",
  "email": "priya@example.com",
  "age": 21,
  "course": 1
}
```

#### Request 3: Get Single Student
```
Method: GET
URL: http://localhost:8000/api/v1/students/1/
```

#### Request 4: Update Student
```
Method: PUT
URL: http://localhost:8000/api/v1/students/1/
Body (JSON):
{
  "name": "Priya Updated",
  "email": "priya_new@example.com",
  "age": 22,
  "course": 2
}
```

#### Request 5: Delete Student
```
Method: DELETE
URL: http://localhost:8000/api/v1/students/1/
```

---

## Part 6: Real-World Usage Scenarios

### Scenario 1: Find all students aged 20+
```python
students = Student.objects.filter(age__gte=20).order_by("name")
print(students)
```

### Scenario 2: Search students by name and sort by age (descending)
```python
query = "rahul"
students = Student.objects.filter(
    name__icontains=query
).order_by("-age")
print(students)
```

### Scenario 3: Get students in a specific course
```python
from students.models import Course

course = Course.objects.get(id=1)
students = Student.objects.filter(course=course).order_by("name")
print(students)
```

### Scenario 4: Complex query - Students aged 18-25 with email from specific domain
```python
from django.db.models import Q

students = Student.objects.filter(
    Q(age__gte=18) & Q(age__lte=25) & Q(email__endswith="@gmail.com")
).order_by("name")
print(students)
```

### Scenario 5: Paginate search results in Django shell
```python
from django.core.paginator import Paginator

students = Student.objects.filter(name__icontains="ra").order_by("name")
paginator = Paginator(students, 5)  # 5 per page

# Get page 1
page1 = paginator.get_page(1)
print(page1.object_list)  # 5 students

# Get total pages
print(paginator.num_pages)
```

---

## Part 7: Checking Django Shell Query Count

```python
# Enable query logging
from django.db import connection
from django.test.utils import CaptureQueriesContext

# Execute query and count
with CaptureQueriesContext(connection) as context:
    students = list(Student.objects.all())

print(f"Total queries: {len(context)}")
for query in context:
    print(query['sql'])
```

---

## Part 8: Common Errors & Solutions

### Error 1: Object Not Found
```python
# ❌ Wrong
student = Student.objects.get(id=999)  # DoesNotExist error

# ✅ Correct
from django.shortcuts import get_object_or_404
student = get_object_or_404(Student, id=999)
```

### Error 2: Multiple Objects Returned
```python
# ❌ Wrong
student = Student.objects.get(name="Rahul")  # MultipleObjectsReturned

# ✅ Correct
students = Student.objects.filter(name="Rahul")
```

### Error 3: Many=True Forgot in Serializer
```python
# ❌ Wrong
serializer = StudentSerializer(students)  # Error with multiple objects

# ✅ Correct
serializer = StudentSerializer(students, many=True)
```

---

## Part 9: Performance Tips

### Use select_related() for ForeignKey
```python
# ❌ Slow (N+1 query problem)
students = Student.objects.all()
for student in students:
    print(student.course.name)  # Extra query per student

# ✅ Fast (1 query)
students = Student.objects.select_related('course').all()
for student in students:
    print(student.course.name)  # No extra queries
```

### Use prefetch_related() for ManyToMany
```python
# ❌ Slow
students = Student.objects.all()
for student in students:
    tags = student.post_set.all()  # Extra query per student

# ✅ Fast
students = Student.objects.prefetch_related('post_set').all()
for student in students:
    tags = student.post_set.all()  # Already loaded
```

### Use only() to fetch specific fields
```python
# ❌ Fetch all
students = Student.objects.all()

# ✅ Fetch only needed fields
students = Student.objects.only('name', 'email')
```

### Use distinct() to remove duplicates
```python
# Remove duplicate results
students = Student.objects.filter(
    Q(age=20) | Q(course__name="Python")
).distinct()
```

---

## Checklist: All Features Working?

- [ ] ORM queries work in Django shell
- [ ] Student list displays with search
- [ ] Sorting dropdown works
- [ ] Pagination works (5 per page)
- [ ] Search + Sort + Pagination combined work
- [ ] Add student form works
- [ ] Edit student form works
- [ ] Delete student confirmation works
- [ ] API GET endpoint returns JSON
- [ ] API POST endpoint creates student
- [ ] API PUT endpoint updates student
- [ ] API DELETE endpoint removes student
- [ ] ViewSet endpoints work
- [ ] Router auto-generates URLs
- [ ] Search in ViewSet works

---

## 🎉 You're Ready!

All 12 Django advanced topics are fully tested and working.

Your application demonstrates:
✅ Professional ORM usage
✅ Class-Based Views best practices
✅ Complete CRUD implementation
✅ Advanced pagination + search
✅ RESTful API design
✅ Modern ViewSet + Router pattern

**Status**: Production Ready! 🚀
