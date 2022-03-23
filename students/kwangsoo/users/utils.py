from my_settings import SECRET_KEY, ALGORITHM

def check_token(func):

    def wrapper(*args, **kwargs):
        if jwt.decode(access_token, SECRET_KEY, algorithm = ALGORITHM):
            return func() 
        else:
            return JsonResponse({"Message: INVALID_TOKEN"}, status = 401)

    return wrapper