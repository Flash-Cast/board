from django import forms
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Report
from django.contrib.auth.forms import UserChangeForm
import os

ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'pdf','docx']  # 許可する拡張子
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB

def validate_file_size(value):
    if value.size > MAX_UPLOAD_SIZE:
        raise ValidationError('ファイルサイズは5MB以下にしてください。')

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1][1:].lower()  # 拡張子を取得
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f'このファイル形式（.{ext}）は許可されていません。')

class UserRegistrationForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="パスワード確認")

    class Meta:
        model = User
        fields = ['username', 'email','password1','password2']

    def clean_email(self):
        allowed_domains = ["ms.saitama-u.ac.jp"]  # 許可するドメイン
        email = self.cleaned_data.get("email")
        domain = email.split('@')[-1]  # メールのドメイン部分を取得
        if domain not in allowed_domains:
            raise ValidationError("このメールドメインは使用できません。")
        return email

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("パスワードが一致しません。")
        return password_confirm

class PostForm(forms.ModelForm):
    file = forms.FileField(validators=[validate_file_extension])  # バリデータを適用
    
    class Meta:
        model = Post
        fields = ['content', 'file', 'name']

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason']

class ProfileEditForm(UserChangeForm):
    # 必要なフィールドだけを表示（例えば、ユーザー名、メール、パスワードなど）
    email = forms.EmailField(required=True)
    password = None  # パスワードを表示しない

    class Meta:
        model = User
        fields = ['username', 'email']