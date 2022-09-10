from django.urls import path
from . import views

urlpatterns=[
 path("",views.dashboard,name="dashboard"),
 path("register/",views.register,name="register"),
 path("login/",views.loginView,name="login"),
 path("logout/",views.logoutView,name="logout"),
 path("dashboard/",views.dashboard,name="dashboard"),
 path("forgotPassword/",views.forgotPassword,name="forgotPassword"),
 path("resetPassword/",views.resetPassword,name="resetPassword"),
 path("validatePassword/<uidb64>/<token>",views.validatePassword,name="validatePassword"),
 path("activate/<uidb64>/<token>",views.activate,name="activate"),


 
#  path("auth_view/",views.auth_with_code,name="auth_view"),
]