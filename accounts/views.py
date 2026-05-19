from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ResetPasswordForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserModel
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import password_validation
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.


class MyLoginView(LoginView):
    template_name = 'account/login.html'
    authentication_form = LoginForm
    def get_success_url(self):
        return reverse_lazy('root:home')

    

# def login_view(request):
#     if request.method == "GET":
#         return render(request, "accounts/login.html")
#     else:
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             try:
#                 user = UserModel.objects.get(email=email)
#             except:
#                 messages.error(request, "user not found")
#                 return redirect("accounts:login")

#             email = user.email
#             user = authenticate(request, username=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect("root:home")
#             else:
#                 messages.error(request, "Invalid username or password")
#                 return redirect("accounts:login")
#         else:
#             messages.error(request, "Invalid form data")
#             return redirect("accounts:login")

#from .models import UserProfile   

# def register_view(request):
#     if request.method == "GET":
#         return render(request, "accounts/register.html") 
#     else:
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             #user = form.save()
#             #profile = UserProfile.objects.create(user=user)
#             #profile.save()
#             messages.success(request, "Registration successful. Please log in.")
#             return redirect("accounts:login")
#         else:
#             messages.error(request, "input data is not valid")
#             redirect (request.path_info)

class RegisterView(CreateView):
    model = UserModel
    form_class = RegisterForm
    template_name = 'accouts/register.html'


@login_required
def logout_view(request):
    logout(request)
    return redirect("root:home")


@login_required
def change_password_view(request):
    if request.method == "GET":
        return render(request, "accounts/change_pass.html") 
    else:
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_pass1 = form.cleaned_data["new_pass1"]
            new_pass2 = form.cleaned_data["new_pass2"]
            if (new_pass1 == new_pass2) and not (request.user.check_password(new_pass1)):
                try :
                    password_validation.validate_password(new_pass1)
                    user = request.user
                    user.set_password(new_pass1)
                    user.save()
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, "password change successfully")
                    return redirect(request.path_info)
                except:
                    messages.add_message(request, messages.ERROR, "validate password not verified")
                    return redirect(request.path_info)
            else:
                messages.add_message(request, messages.ERROR, "pass1 and 2 must be same or new pass could not be as old pass")
                return redirect(request.path_info)
        else:
            messages.add_message(request, messages.ERROR, "input data is not valid")
            return redirect(request.path_info)

                

def reset_password(request):
    if request.method == "GET":
        return render(request, "accounts/reset_password.html") 
    else:
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = UserModel.objects.get(email=email)
            token, create = Token.objects.get_or_create(user=user)
            send_mail(
                "reset password",
                f"http://127.0.0.1:8000/accounts/reset-password-confirm/{token.key}",
                "admin@site.test",
                [user.email],
                fail_silently=True
            )
            return redirect("accounts:reset-password-done")



    



def reset_password_done(request):
    return render(request, "accounts/reset_password_done.html") 


def reset_password_confirm(request, token):
    if request.method == "GET":
        return render(request, "accounts/reset_password_confirm.html") 
    else:
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_pass1 = form.cleaned_data["new_pass1"]
            new_pass2 = form.cleaned_data["new_pass2"]
            user = Token.objects.get(key=token).user
            if (new_pass1 == new_pass2) and not (user.check_password(new_pass1)):
                try :
                    password_validation.validate_password(new_pass1)
                    user.set_password(new_pass1)
                    user.save()
                    return redirect("accounts:reset-password-complete")
                except:
                    messages.add_message(request, messages.ERROR, "validate password not verified")
                    return redirect(request.path_info)
            else:
                messages.add_message(request, messages.ERROR, "pass1 and 2 must be same or new pass could not be as old pass")
                return redirect(request.path_info)
        else:
            messages.add_message(request, messages.ERROR, "input data is not valid")
            return redirect(request.path_info)


def reset_password_complete(request):
    return render(request, "accounts/reset-password-complete.html") 
