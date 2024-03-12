from django.urls import path
from .views import create_student,get_single_student,get_all_students,delete_student,update_student, upload_img,serve_image

urlpatterns = [
    path('create-student', create_student),
    path('upload-img', upload_img),
    path('get-img/<int:student_id>', serve_image),
    path('get-single-student/<int:student_id>/', get_single_student),
    path('get-all-students', get_all_students),
    path('delete-student/<int:student_id>', delete_student),
    path('update-student/<int:student_id>', update_student),

]