import json

from django.views import View

class PostingView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            content = data['content']
            
            user = 
            img_url

            Post.objects.create()

        except KeyError: