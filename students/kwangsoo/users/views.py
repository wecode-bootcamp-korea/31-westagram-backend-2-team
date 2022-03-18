import json
import re

from django.http  import JsonResponse
from django.views import View

from users.models import User

class UserView(View):
    def post(self, request):
        try:
            data = Json.loads(request.body)

            name         = data['name']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']
            created_at   = data['created_at']
            updated_at   = data['updated_at']
          
            emailchecker = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
            passwordchecker = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")

            if emailchecker.match(email) == None:
                return JsonResponse({'Message' : 'Not a valid email'}, status = 400)

            elif passwordchecker.match(password) == None:
                return JsonResponse({'Message' : 'Not a valid password. Password must be more than eight characters including any character, number and speical characters'}, status = 400)

            else:
                User.objects.create(
                    name = name
                    email = email
                    password = password
                    phone_number = phone_number
                    created_at = created_at
                    updated_at = updated_at
                )
                return JsonResponse('message' : 'SUCCESS', status = 201)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
