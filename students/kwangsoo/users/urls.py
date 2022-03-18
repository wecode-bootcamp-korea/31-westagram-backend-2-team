from django.urls import path, include
from .views import UserView

urlpatterns = {
    path('/registration', UserView.as_view()) 
}