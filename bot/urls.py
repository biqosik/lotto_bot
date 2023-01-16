from . import views
from django.urls import path
urlpatterns = [
    path('', views.home, name="home"),
    path('login_user', views.login_user, name="login"),
]