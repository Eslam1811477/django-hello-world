from django.urls import path
from .views import create_student,get_single_student,get_all_students,delete_student,update_student

urlpatterns = [
    path('create-student', create_student),
    path('get-single-student/<int:student_id>/', get_single_student),
    path('get-all-students', get_all_students),
    path('delete-student/<int:student_id>', delete_student),
    path('update-student/<int:student_id>', update_student),

]