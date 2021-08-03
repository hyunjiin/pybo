from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):  #UserCreationForm을 그대로 사용해도 되지만 이메일 등의 부가속성을 만들기 위해 UserCreationForm 상속해서 클래스 생성
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")