import json, re, bcrypt, jwt

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
            hashed_pw    = hashed_pw.decode('utf-8')
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
            return JsonResponse({'Message' : 'SUCCESS'}, status = 201)

        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status = 400)



class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email     = data['email']
            password  = data['password']

            user = User.objects.get(email=eamil)

            db_password = user.password

            if not User.objects.get(email=email):
                return JsonResponse({"Message" : "EMAIL_NOT_REGISTERED"}, status = 401)

            if not bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8')):
                return JsonResponse({"Message" : "INVLID_PASSWORD"}, status = 401)

            SECRET = 
            access_token = jwt.encode({"id" : user.id, SECRET, algorithm = "HS256"})

            return JsonResponse({"Message" : "SUCCESS"}, {"token" = access_token} , status = 200)

        except KeyError:
            return JsonResponse({"Message" : "KEY_ERROR"}, status = 400)
