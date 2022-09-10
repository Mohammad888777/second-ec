from django.shortcuts import render,redirect
from .forms import SignUpForm
from .models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from codes.forms import CodeForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator    
from django.http import HttpResponse,HttpResponseRedirect
from .decorators import login_need,no_need_login



@no_need_login
def register(request):

    form=SignUpForm()
   
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data.get("first_name")
            last_name=form.cleaned_data.get("last_name")
            email=form.cleaned_data.get("email")
            phone_number=form.cleaned_data.get("phone_number")
            password=form.cleaned_data.get("password")
            username=email.split('@')[0]
            # confirm_password=form.cleaned_data.get("confirm_password")

            user=User.objects.create_user(
                first_name=first_name,last_name=last_name,username=username,email=email,password=password
            )
            user.phone_number=phone_number
            user.is_active=False
            user.save()

            curret_site=get_current_site(request)
            mail_subject="plaese activate your account"
            message=render_to_string("accounts/activate_account.html",{
                'user':user.username,
                'domin':curret_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            }); 
            mail=email
            email_to_be_send=EmailMessage(mail_subject,message,to=[mail])
            email_to_be_send.send()

            # messages.success(request,"your account is saved now")
            return redirect("/accounts/login/?command=verification&email="+email[:5]+'...')
        else:
            messages.error(request,"your form is not valid")
            return redirect("register")
            
    contex={
        'form':form
        }

    return render(request,"accounts/register.html",contex)


def loginView(request):

    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        print(email,"EEEEEEEEEEEEEEEEEEEEEE")
        print(password,"PPPPPPPPPPPPPPPP")
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request,"username or email does not exsist")
            return redirect("login")
        else: 
            user=authenticate(email=email,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,"login successfully")
                # request.session["pk"]=user.pk

                return redirect('dashboard')
            else:
                messages.warning(request,"not correct username or email")

    return render(request,"accounts/login.html",)



@login_need
def logoutView(request):
    logout(request)
    return redirect("login")




def activate(request,uidb64,token):

    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
        
    except (ValueError,TypeError,OverflowError,User.DoesNotExist) :
        user=None
    if user is not None and default_token_generator.check_token(user,token) :
        user.is_active=True
        user.save()
        messages.success(request,"your account is verfied successfully")
        return redirect("login")
    else:
        messages.error(request,"your activation code is incorrect send agein")
        return redirect("register")
    # return redirect("login")



@login_need
def dashboard(request):
    
    return render(request,"accounts/dashboard.html")



def forgotPassword(request):

    if request.method=="POST":
        email=request.POST.get("email")
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email__exact=email)
            curret_site=get_current_site(request)
            mail_subject="Reset your Password"
            message=render_to_string("accounts/reset_password_email.html",{
                'user':user.username,
                'domin':curret_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            }); 
            mail=email
            email_to_be_send=EmailMessage(mail_subject,message,to=[mail])
            email_to_be_send.send()
            messages.success(request,"new Code is send to your email")
            return redirect("login")
        else:
            messages.error(request,"Email does not exists")
            return redirect("forgotPassword")

    return render(request,"accounts/forgotPassword.html")



def validatePassword(request,uidb64,token):

    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User._default_manager.get(pk=uid)
    except (ValueError,TypeError,OverflowError,User.DoesNotExist) :
        user=None
    if user is not None and user.is_active and default_token_generator.check_token(user,token):
        request.session["uid"]=uid
        messages.success(request,"please reset your Pasword")
        return redirect("resetPassword")
    else:
        messages.error(request,"this link is expired")
        return redirect("login")



def resetPassword(request):
    if request.method=="POST":
        password=request.POST.get("password")
        confirm_password=request.POST.get("confirm_password")

        if password == confirm_password:
            uid=request.session.get("uid")
            user=User.objects.get(pk=uid)
            if user:
                user.set_password(password)
                user.save()
                messages.success(request,"your new Password is et now")
                return redirect("login")
        else:
            messages.error(request,"password does not match")
            return redirect(request.META.get("HTTP_REFERER"))

    return render(request,"accounts/resetPassword.html")






def auth_with_code(request):
    form=CodeForm(request.POST or None)
    contex={'form':form}   
    pk=request.session.get("pk")

    user=User.objects.get(pk=pk)
    if user:
        code=user.code
        code_user=f"user is {user.username} and code is {code} "
        if not request.POST:
            print(code_user)
        if form.is_valid():
            num=request.POST.get("number")
            if str(num)==str(code):
                code.save()
                login(request,user)
                return redirect("home")
            else:
                return redirect("auth_view")

    return render(request,"accounts/auth_with_code.html",contex)


