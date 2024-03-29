from .models import Student
from django.http import JsonResponse
import os
import secrets
from django.views.static import serve
from django.conf import settings
import json
from django.core.serializers import serialize
from utils.jwt import jwt_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods


@csrf_exempt
@require_http_methods(["POST"])
@jwt_required
def create_student(request):
    res = {
        'data': {},
        'msg': '',
        'actionDone': False
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        date_of_birth = request.POST.get('date_of_birth')
        national_ID = request.POST.get('national_ID')
        phone_number = request.POST.get('phone_number')
        mother_name = request.POST.get('mother_name')
        father_name = request.POST.get('father_name')
        mother_phone_number = request.POST.get('mother_phone_number')
        father_phone_number = request.POST.get('father_phone_number')
        gender = request.POST.get('gender')

        if not name or not date_of_birth or not national_ID:
            res['msg'] = 'Invalid student registration data'
        else:
            try:
                Student.objects.get(name=name)
                res['msg'] = 'Name already taken'
            except Student.DoesNotExist:
                new_student = Student.objects.create(
                    name=name,
                    date_of_birth=date_of_birth,
                    national_ID=national_ID,
                    phone_number=phone_number,
                    mother_name=mother_name,
                    father_name=father_name,
                    mother_phone_number=mother_phone_number,
                    father_phone_number=father_phone_number,
                    gender=gender,
                )
                new_student.save()

                res['data'] = {
                    'id': new_student.id,
                    'name': new_student.name,
                    'date_of_birth': new_student.date_of_birth,
                    'national_ID': new_student.national_ID,
                    'phone_number': new_student.phone_number,
                    'mother_name': new_student.mother_name,
                    'father_name': new_student.father_name,
                    'mother_phone_number': new_student.mother_phone_number,
                    'father_phone_number': new_student.father_phone_number,
                    'gender': new_student.gender,
                }

                res['msg'] = 'Student registration successful'
                res['actionDone'] = True
    else:
        res['msg'] = 'Invalid request method'

    return JsonResponse(res)

@csrf_exempt
@require_http_methods(["POST"])
@jwt_required
def upload_img(request):
    res = {
        'data': {},
        'msg': '',
        'actionDone': False
    }
    try:
        image = request.FILES.get('image')
        stu_id = request.POST.get('id')
        
        _, file_extension = os.path.splitext(image.name)

        filename = secrets.token_hex(5) + file_extension.lower()
        save_path = os.path.join(settings.MEDIA_ROOT, filename)

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)

        image_url = os.path.join(settings.MEDIA_URL, filename)
        student = Student.objects.get(id=stu_id)

        if student:
            student.img_name = filename
            student.save()

            res['data']['image_url'] = image_url
            res['msg'] = 'The image has been uploaded successfully'
            res['actionDone'] = True
        else:
            res['msg'] = 'Student not found'

    except Exception as e:
        res['msg'] = f'Error: {str(e)}'
        res['actionDone'] = False

    return JsonResponse(res)


@csrf_exempt
@require_http_methods(["GET"])
@jwt_required
def serve_image(request, student_id):
    student = Student.objects.get(id=student_id)
    if(student):
        return serve(request, student.img_name, document_root=settings.MEDIA_ROOT)
    else:
        return JsonResponse({
                'msg': 'Student number not found',
                'actionDone': False
        })







@jwt_required
@require_http_methods(["GET"])
def get_all_students(request):
    res = {
        'data': {},
        'msg': '',
        'actionDone': False
    }

    if request.method == 'GET':
        students = Student.objects.all()

        serialized_students = serialize('json', students)

        students_data = json.loads(serialized_students)

        res['data'] = students_data
        res['msg'] = 'All students retrieved successfully'
        res['actionDone'] = True
    else:
        res['msg'] = 'Invalid request method'

    return JsonResponse(res)


@jwt_required
@require_http_methods(["GET"])
def get_single_student(request, student_id):
    res = {
        'data': {},
        'msg': '',
        'actionDone': False
    }

    if request.method == 'GET':
        try:
            student = Student.objects.get(id=student_id)
            serialized_student = serialize('json', [student])
            student_data = json.loads(serialized_student)[0]['fields']
            
            res['data'] = student_data
            res['msg'] = 'Student retrieved successfully'
            res['actionDone'] = True
        except Student.DoesNotExist:
            res['msg'] = 'Student not found'
    else:
        res['msg'] = 'Invalid request method'

    return JsonResponse(res)



@csrf_exempt
@jwt_required
@require_http_methods(["DELETE"])
def delete_student(request,student_id):
    res = {
        'data': {},
        'msg': '',
        'actionDone': False
    }

    try:
        if not student_id:
            raise ValueError("student_id is missing in form data")

        student = Student.objects.get(id=student_id)
        student.delete()
        res['msg'] = 'Student deleted successfully'
        res['actionDone'] = True
    except ValueError as ve:
        res['msg'] = str(ve)
    except Student.DoesNotExist:
        res['msg'] = 'Student not found'

    return JsonResponse(res)

@jwt_required
@require_http_methods(["GET"])
def students_search(request):
    body_unicode = request.body.decode('utf-8')
    
    if body_unicode:
        data = json.loads(body_unicode)
        
        name = data.get('name', '')
        school = data.get('school', '')
        
        students = Student.objects.all()
        
        if name:
            students = students.filter(name__icontains=name)
        if school:
            students = students.filter(school__icontains=school)
        
        results = [{'name': student.name, 'pk':student.pk} for student in students]
        
        response_data = {
            'data': results,
            'msg': 'Search successful',
            'actionDone': True
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'No JSON data received.'}, status=400)


@csrf_exempt
@jwt_required
@require_http_methods(["PUT"])
def update_student(request, student_id):
    res = {
        'data': {},
        'msg': '',
        'actionDone': False
    }

    try:
        if not student_id:
            raise ValueError("student_id is missing")
        student = Student.objects.get(id=student_id)
        updated_data = json.loads(request.body.decode('utf-8'))

        print(updated_data)

        for key, value in updated_data.items():
            setattr(student, key, value)

        student.save()

        res['msg'] = 'Student updated successfully'
        res['actionDone'] = True
    except ValueError as ve:
        res['msg'] = str(ve)
    except Student.DoesNotExist:
        res['msg'] = 'Student not found'

    return JsonResponse(res)
