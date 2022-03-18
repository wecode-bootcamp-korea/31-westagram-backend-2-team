from django.urls import path

from users.views import UserView

urlpatterns=[
    path('/userlist', UserView.as_view())
]