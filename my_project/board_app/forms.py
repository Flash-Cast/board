from django import forms
from .models import Post, Thread, Report
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
import os

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'pdf', 'docx', 'xlsx']
MAX_UPLOAD_SIZE = 30 * 1024 * 1024  # 30MB

def validate_file_size(value):
    if value.size > MAX_UPLOAD_SIZE:
        raise ValidationError('ファイルサイズは30MB以下にしてください。')

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1][1:].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f'このファイル形式（.{ext}）は許可されていません。')

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        allowed_domains = ["ms.saitama-u.ac.jp"]
        email = self.cleaned_data.get("email")

        domain = email.split('@')[-1]
        if domain not in allowed_domains:
            raise ValidationError("このメールドメインは使用できません。")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        password_confirm = cleaned_data.get("password2")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("パスワードが一致しません。")

        return cleaned_data

class PostForm(forms.ModelForm):
    file = forms.FileField(validators=[validate_file_extension, validate_file_size], required=False)

    class Meta:
        model = Post
        fields = ['content', 'file', 'name']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason']

class ProfileEditForm(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = ['password']  # パスワードをフォームに表示しない

class ThreadForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Thread
        fields = ['title', 'content', 'file', 'category']
