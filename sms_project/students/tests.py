from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from students.models import Student, Course

class StudentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='modeluser', password='password123')
        self.course = Course.objects.create(name="Computer Science")
        self.student = Student.objects.create(
            name="Test Student",
            email="test@example.com",
            age=20,
            course=self.course,
            created_by=self.user
        )

    def test_student_creation(self):
        self.assertEqual(self.student.name, "Test Student")
        self.assertEqual(str(self.student), "Test Student")

    def test_course_creation(self):
        self.assertEqual(str(self.course), "Computer Science")

class StudentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='viewuser', password='password123')
        self.client.login(username='viewuser', password='password123')
        self.course = Course.objects.create(name="Engineering")
        Student.objects.create(name="Alice", email="alice@example.com", age=22, course=self.course, created_by=self.user)
        Student.objects.create(name="Bob", email="bob@example.com", age=21, course=self.course, created_by=self.user)

    def test_student_list_view(self):
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice")
        self.assertContains(response, "Bob")

    def test_student_search(self):
        response = self.client.get(reverse('student_list') + '?search=Alice')
        self.assertContains(response, "Alice")
        self.assertNotContains(response, "Bob")

class StudentAPITest(APITestCase):
    def setUp(self):
        self.course = Course.objects.create(name="Mathematics")
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.student_data = {
            "name": "API Student",
            "email": "api@example.com",
            "age": 25,
            "course": self.course.id
        }

    def test_get_students_list_unauthenticated(self):
        """Unauthenticated users should be able to LIST students (ReadOnly)."""
        response = self.client.get('/api/v1/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_student_unauthenticated(self):
        """Unauthenticated users should NOT be able to CREATE students."""
        response = self.client.post('/api/v1/students/', self.student_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_student_authenticated(self):
        """Authenticated users should be able to CREATE students."""
        self.client.login(username='testuser', password='password123')
        response = self.client.post('/api/v1/students/', self.student_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.get().name, "API Student")
