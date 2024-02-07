from django.urls import path
from .views import create_student,get_single_student,get_all_students

urlpatterns = [
    path('create-student', create_student),
    path('get-single-student/<int:student_id>/', get_single_student),
    path('get-all-students', get_all_students),
]