from . import views
from django.urls import path
from django.views.i18n import JavaScriptCatalog
urlpatterns = [
    path('', views.home, name="home"),
    path('login_user', views.login_user, name="login"),
    path('logout', views.logout_user, name = "logout"),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]