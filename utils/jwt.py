import jwt
from env_data import env_data
from django.http import HttpResponseBadRequest
from functools import wraps

def generate_token(_id,name):
    payload = {'_id': _id,'name':name}
    token = jwt.encode(payload,env_data['SECRET_KEY'], algorithm='HS256')
    return token



def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        
        jwt_token = request.headers.get('Authorization')
        try:
            decoded_token = jwt.decode(jwt_token, env_data['SECRET_KEY'], algorithms=['HS256'])
            request.jwt_data = decoded_token  
        except jwt.ExpiredSignatureError:
            return HttpResponseBadRequest("JWT has expired")
        except jwt.InvalidTokenError:
            return HttpResponseBadRequest("Invalid JWT")

        return view_func(request, *args, **kwargs)

    return _wrapped_view