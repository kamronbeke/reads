from django import forms
from django.contrib.auth.models import User


#
#
#
# class RegisterForm(forms.Form):
#     username = forms.CharField(max_length=150)
#     first_name = forms.CharField(max_length=150)
#     last_name = forms.CharField(max_length=150)
#     email = forms.EmailField()
#     password = forms.CharField(max_length=126)


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name', 'password')

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()

        return user



class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128)

