from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import student_list, student_detail, StudentViewSet

# ============================================================================
# ROUTER SETUP - Automatic URL Generation (Day 20)
# ============================================================================
# DefaultRouter automatically generates URLs for ViewSet
# One router replaces all manual URL definitions!

router = DefaultRouter()
router.register('students', StudentViewSet)  # Automatically creates all CRUD URLs

# Generated URLs by router:
# GET      /api/v1/students/           → List all students
# POST     /api/v1/students/           → Create new student
# GET      /api/v1/students/{id}/      → Retrieve single student
# PUT      /api/v1/students/{id}/      → Update student (full)
# PATCH    /api/v1/students/{id}/      → Partial update
# DELETE   /api/v1/students/{id}/      → Delete student

urlpatterns = [
    # ========== ROUTER ENDPOINTS (Recommended - Modern Approach) ==========
    path('v1/', include(router.urls)),  # New ViewSet-based API endpoints
    
    # ========== LEGACY ENDPOINTS (Kept for backward compatibility) ==========
    path('students-api/', student_list),
    path('students-api/<int:pk>/', student_detail),
]
