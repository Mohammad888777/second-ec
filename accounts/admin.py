from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display=["email","first_name","last_name","username","last_login","date_joined","is_active"]
    filter_horizontal=()
    list_filter=[]
    fieldsets=[]
    readonly_fields=["last_login","date_joined"]
    list_display_links=["email","first_name","last_name"]
    ordering=["-date_joined"]
    
admin.site.register(User,CustomUserAdmin)