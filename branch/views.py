from utils.jwt import jwt_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Branch

# Create your views here.



@csrf_exempt
@require_http_methods(["POST"])
@jwt_required
def add_branch(request):
    res = {
        'data': {},
        'msg': '',
        'actionDone': False
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        zone = request.POST.get('zone')
        Initial_budget = request.POST.get('initial budget')


        if not name or not zone:
                res['msg'] = 'Invalid branch registration data'
        else:
            try:
                Branch.objects.get(name=name)
                res['msg'] = 'Name already taken'
            except Branch.DoesNotExist:
                new_branch = Branch.objects.create(
                    name=name,
                    zone=zone,
                    budget=Initial_budget,
                )

                new_branch.save()

                res['data'] = {
                    'id': new_branch.id,
                    'name': new_branch.name,
                    'zone': new_branch.zone,
                    'budget': new_branch.budget,
                }
                res['msg'] = 'Branch registration successful'
                res['actionDone'] = True
    else:
        res['msg'] = 'Invalid request method'

    return JsonResponse(res)

