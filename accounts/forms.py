from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm, SetPasswordForm
from allauth.account.forms import SignupForm, LoginForm
from .models import User

class MyCustomSignupForm(SignupForm):
    position = forms.CharField(max_length=15)
    user_image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # django-allauthのフィールドを上書き
        self.fields['username'].widget.attrs['placeholder'] = '8文字以下'
        self.fields['position'].widget.attrs['placeholder'] = '15文字以下'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレス'
        self.fields['password1'].widget.attrs['placeholder'] = '8文字以上の十分に複雑なもの'
        self.fields['password2'].widget.attrs['placeholder'] = '8文字以上の十分に複雑なもの'

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'position', 'user_image']


    def save(self, request):

        user = super(MyCustomSignupForm, self).save(request)

        user.position = request.POST.get('position')
        user.user_image = request.FILES.get('user_image')
        user.save()

        return user

class MyCustomLoginForm(LoginForm):


    def login(self, *args, **kwargs):

        return super(MyCustomLoginForm, self).login(*args, **kwargs)

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email',  'position', 'user_image']
