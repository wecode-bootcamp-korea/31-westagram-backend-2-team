import json, re, bcrypt, jwt

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

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
                return JsonResponse({"message" : "INVAILD_EMAIL"}, status = 400)

            if not re.match(REGEX_PASSWORD, password):
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 400)

            if User.objects.filter(email = email).exists():
                return JsonResponse({"message" : "REGISTERED_EMAIL"}, status = 400)

            hashed_password  = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                name         = name,
                email        = email,
                password     = hashed_password,
                phone_number = phone_number,
            )
            return JsonResponse({"message" : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)



class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']

            user           = User.objects.get(email = email)
            db_password    = user.password
            password_check = bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8'))

            if not password_check:
                return JsonResponse({"message" : "INVALID_PASSWORD"}, status = 401)

            access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

            return JsonResponse({"message" : "SUCCESS", "token" : access_token}, status = 200)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status = 401)