from django.http import JsonResponse
from .models import User
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import User
from utils.jwt import generate_token,jwt_required
from utils.password import check_pass,hash_pass
from django.views.decorators.csrf import csrf_exempt




@csrf_exempt
def get_all_users(req):
    data = {'message': 'Hello, this is a JSON response!', 'items': []}
    return JsonResponse(data)






def initialize_users():
    # Check if admin user exists
    admin_user, created = User.objects.get_or_create(
        name='admin',
        defaults={'password': hash_pass('12345'), 'permission': 'admin'}
    )

    if created:
        print("Admin user created.")
    else:
        print("Admin user already exists.")

# initialize_users()



@csrf_exempt
def user_login_view(request):
    res = {
        'data': {},
        'msg': '',
        'actionDone': False
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        if not name or not password:
            res['msg'] = 'Invalid name or password'
        else:
            user = get_object_or_404(User, name=name)

            if check_pass(password, user.password):
                res['data'] = {'name': user.name, 'permission': user.permission, 'token': generate_token(user.id, user.name)}
                res['msg'] = 'Login successful'
                res['actionDone'] = True
            else:
                res['msg'] = 'Invalid name or password'
    else:
        res['msg'] = 'Invalid request method'

    return JsonResponse(res)

@csrf_exempt
@jwt_required
def create_user(request):
    res = {
    'data': {},
    'msg': '',
    'actionDone': False
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        permission = request.POST.get('permission')

        if not name or not password or not permission:
            res['msg'] = 'Invalid user registration data'
        else:
            try:
                User.objects.get(name=name)
                res['msg'] = 'name already taken'
            except User.DoesNotExist:
                hashed_password = hash_pass(password)

                new_user = User.objects.create(
                    name=name,
                    password=hashed_password,
                    permission=permission,
                )
                new_user.save()

                res['data'] = {'name': new_user.name, 'permission': new_user.permission}
                res['msg'] = 'User registration successful'
                res['actionDone'] = True
    else:
        res['msg'] = 'Invalid request method'

    return JsonResponse(res)