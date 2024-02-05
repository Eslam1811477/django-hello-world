from .models import Student
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.jwt import jwt_required


@csrf_exempt
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
