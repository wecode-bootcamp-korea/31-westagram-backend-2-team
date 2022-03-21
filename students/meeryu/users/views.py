import json
import re

from django.http  import JsonResponse
from django.views import View

from .models import User

class SignUpView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

            email    = data['email']
            password = data['password']
 
            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({"message" : "INVALID_EMAIL"}, status = 400)

            if User.objects.filter(email = email):
                return JsonResponse({"message" : "EMAIL_ALREADY_EXISTS"}, status = 400)

            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 400)
            
            User.objects.create(
                name         = data['name'],
                email        = data['email'],
                password     = data['password'],
                phone_number = data['phone_number']
            )
            return JsonResponse({"message" : "SUCCESS"}, status = 201)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400) 
            
class SignInView(View):
    def post(self,request):
            try: 
                data  = json.loads(request.body)

                if User.objects.filter(email=data['email'], password=data['password']).exists():
                    return JsonResponse({"message":"SUCCESS"}, status=201)

                return JsonResponse({"message": "INVALID_USER"}, status=401)

            except KeyError:
                return JsonResponse({"message":"KEYERROR"}, status = 400)