from django import forms
from django.core.mail import send_mail

from users.models import CustomUser





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
        model = CustomUser
        fields = ('username','email','first_name','last_name', 'password')

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()

        if user.email:
            send_mail(
                'Your Goodreads account has been created.',
                'Welcome to Goodreads clone!',
                'ikromjon01021995@gmail.com',
                [user.email],
            )




class UserLoginForm(forms.Form):
    class Meta:
        model = CustomUser
        fields = ('username','password')




class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_picture')

