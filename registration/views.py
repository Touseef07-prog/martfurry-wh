from django.shortcuts import render, redirect
from django.views import View
from registration.forms import UserForm, UserLoginForm
from django.contrib import messages, auth
from registration.models import CustomUser

from django.utils.translation import gettext_lazy as _

class RegisterUser(View):
    def get(self, request, *args, **kwargs):
        active = kwargs.pop('active', 'login')
        context = {
            'signup_form': UserForm(),
            'login_form': UserLoginForm(),
            'active': active
        }
        return render(request, 'registration/loginAndRegister.html', context=context)


class CreateUser(RegisterUser):
    def get(self, request, *args, **kwargs):
        return super().get(request, active='register', *args, **kwargs)

    def post(self, request, *args, **kwargs):
        signup_form = UserForm(request.POST)
        context = {
            'signup_form': UserForm(),
            'login_form': UserLoginForm(),
            'active': 'register'
        }
        email = request.POST['email']
        password = request.POST['password1']
        if signup_form.is_valid():
            signup_form.save()
            user = auth.authenticate(
                request, username=email, password=password)
            auth.login(request, user)
            messages.success(request, _("Thank you for registration"))
            return redirect('pages:home')
        else:
            errorStr = ""
            errorDict = dict(signup_form.errors)
            for i in errorDict:
                errorStr += errorDict[i]
            messages.error(request, errorStr)
            return render(request, 'registration/loginAndRegister.html', context=context)


class LoginUser(RegisterUser):
    def get(self, request, *args, **kwargs):
        return super().get(request, active='login', *args, **kwargs)

    def post(self, request, *args, **kwargs):
        login_from = UserLoginForm(request.POST)
        context = {
            'signup_form': UserForm(),
            'login_form': UserLoginForm(),
            'active': 'login'
        }
        if login_from.is_valid():
            user = auth.authenticate(
                request, email=request.POST['email'], password=request.POST['password'])
            if not user:
                messages.error(
                    request, _("Please enter a correct email address and password. Note that both fields may be case-sensitive."))
                return render(request, 'registration/loginAndRegister.html', context=context)
            auth.login(request, user)
            messages.success(request, _("You are currently logged in"))
            return redirect('pages:home')
        else:
            messages.error(request, _("Something went wrong. Please try again."))
            return render(request, 'registration/loginAndRegister.html', context=context)
