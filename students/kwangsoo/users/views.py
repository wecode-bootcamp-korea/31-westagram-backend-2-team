import json
import re
import bcrypt

from django.http  import JsonResponse
from django.views import View

from users.models import User

class RegistrationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            name         = data['name']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']
           
            REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

        
            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({'Message' : 'INVAILD_EMAIL'}, status = 400)

            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({'Message' : 'INVALID_PASSWORD'}, status = 400)

            if User.objects.filter(email = email).exists():
                return JsonResponse({'Message' : 'REGISTERED_EMAIL'}, status = 400)

            hashed_pw    = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            hashed_pw    = hashed_pw.decode('utf-8')

            User.objects.create(
                name         = name,
                email        = email,
                password     = password,
                phone_number = phone_number,
            )
            return JsonResponse({'message' : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)



class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']

            if not User.objects.filter(email = email, password = password):
                return JsonResponse({"message" : "INVALID_USER"}, status = 401)

            return JsonResponse({"message" : "SUCCESS"}, status = 200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
