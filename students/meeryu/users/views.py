import json
import re
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from .models import User

class SignUpView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            REGEX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

            name         = data['name']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']
 
            if not re.match(REGEX_EMAIL, email):
                return JsonResponse({"message" : "INVALID_EMAIL"}, status = 400)

            if User.objects.filter(email = email):
                return JsonResponse({"message" : "EMAIL_ALREADY_EXISTS"}, status = 400)

            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
            User.objects.create(
                name         = name,
                email        = email,
                password     = hashed_password,
                phone_number = phone_number
            )
            return JsonResponse({"message" : "SUCCESS"}, status = 201)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400) 
            
class SignInView(View):
    def post(self,request):
            try: 
                data     = json.loads(request.body)
                email    = data['email']
                password = data['password'] 
                
                if not User.objects.filter(email = email):
                    return JsonResponse({"message" : "INVALID_USER"}, status = 401)

                input_password  = User.objects.get(email = email).password
                check_password  = bcrypt.checkpw(password.encode('utf-8'), input_password.encode('utf-8'))
                if not check_password:
                    return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 401)

                payload      = User.objects.get(email = email).id
                access_token = jwt.encode({"id" : payload}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
                return JsonResponse({
                    "message" : "SUCCESS",
                    "token" : access_token
                    }, status = 200)

            except KeyError:
                return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
                