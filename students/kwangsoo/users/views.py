import json
import re
import bcrypt

from django.http  import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

from users.models import User

class RegistrationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            name         = data['name']
            email        = data['email']
            password     = data['password']
            hashed_pw    = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            phone_number = data['phone_number']
           
            REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

        
            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({'Message' : 'INVAILD_EMAIL'}, status = 400)

            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({'Message' : 'INVALID_PASSWORD'}, status = 400)

            User.objects.create(
                name         = name,
                email        = email,
                password     = hashed_pw,
                phone_number = phone_number,
            )
            return JsonResponse({'message' : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)



class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email     = data['email']
            password  = data['password']

            db_password = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode('utf-8'), db_password):
                return JsonResponse({"message" : "INAVLID_USER"})

            return JsonResponse({"message" : "SUCCESS"}, status = 200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
