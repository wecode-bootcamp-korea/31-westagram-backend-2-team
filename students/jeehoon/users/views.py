import json
import re

from django.http  import JsonResponse
from django.views import View

from users.models import User

class SignUpView(View):
    def post(self, request):
        try: 
            data                = json.loads(request.body)
            email_validation    = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
            password_validation = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")
            
            if email_validation.match(data['email']) == None :
                return JsonResponse({'Message' : 'Email Validation'}, status=400)
            
            if password_validation.match(data['password']) == None : 
                return JsonResponse({'Message' : 'Password Validation'}, status=400)
            
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'Message' : 'Email already exists'}, status=401)
        
            User.objects.create(
                name         = data['name'],
                email        = data['email'],
                password     = data['password'],
                phone_number = data['phone_number'],
            )
            return JsonResponse({'Message' : 'Success'}, status=201)
        except KeyError:
            return JsonResponse({'Message' : 'Key_Error'}, status=400)