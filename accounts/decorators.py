from django.http import Http404
from django.shortcuts import render,get_object_or_404,redirect
from .models import User
from functools import wraps


def no_need_login(func):
    @wraps(func)
    def inner(request,*args,**kwargs):
        if request.user.is_anonymous  and request.user.pk ==None and not request.user.is_active :
            return func(request,*args,**kwargs)
        else:
            return redirect("home")
    return inner




def login_need(func):
    @wraps(func)
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated and request.user.pk !=None and request.user.is_active :
            return func(request,*args,**kwargs)
        else:
            return redirect("login")
    return inner

