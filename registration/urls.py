from django.urls import path
from django.contrib.auth.views import LogoutView

from registration.views import RegisterUser,LoginUser,CreateUser
from registration.forms import UserPasswordResetForm,UserPasswordChangeForm
import django.contrib.auth.views as auth_views


urlpatterns = [
    path('', RegisterUser.as_view(),name='loginAndRegister'),
    path('login/', LoginUser.as_view(),name='login'),
    path('register/', CreateUser.as_view(),name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=UserPasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=UserPasswordChangeForm), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')

]
