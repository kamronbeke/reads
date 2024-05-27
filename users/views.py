from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from django.shortcuts import render, redirect
from django.views import View
from users.forms import UserCreateForm, UserLoginForm, UpdateProfileForm



class RegisterView(View):
    def get(self, request):
        create_user = UserCreateForm()

        context = {
            'form':create_user
        }
        return render(request=request, template_name='users/register.html', context=context)

    def post(self, request):
        create_form = UserCreateForm(data=request.POST)

        if create_form.is_valid():
            create_form.save()
            return redirect('users:login')
        else:
            context = {
                'form': create_form
            }
            return render(request=request, template_name='users/register.html', context=context)


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()

        return render(request=request, template_name='users/login.html',context= {'form' : login_form})

    def post(self, request):

        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, f'Welcome {user.username}')


            return redirect('landing_page')
        else:
            return render(request=request, template_name='users/login.html',context= {'form' : login_form})





class ProfileView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'users/profile.html', {'user': request.user})



class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('landing_page')


class UpdateProfileView(LoginRequiredMixin, View):
    def get(self, request):
        userform = UpdateProfileForm(instance=request.user)

        return render(request, 'users/profile_update.html', {'form': userform})

    def post(self, request):
        user = UpdateProfileForm(instance=request.user,
                                 data=request.POST,
                                 files=request.FILES
                                 )
        if user.is_valid():
            user.save()
            messages.success(request, "O'zgarishlar saqlandi")
            return redirect('users:profile')
        return render(request, 'users/profile_update.html', {'form': user})
