from django import forms
from django.contrib.auth import authenticate

from book_store.utils import validate_email
from user_access.models import User


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields['email'].error_messages['required'] = 'Email is required'
            self.fields['password'].error_messages['required'] = 'Password is required'

    def clean_password(self):
        email = self.cleaned_data.get('email').lower()
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password")
            if not user.is_active:
                raise forms.ValidationError("Invalid login")
        else:
            raise forms.ValidationError("Email and Password required")
        return password


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower()
            email_valid = validate_email(email)
            if not email_valid:
                raise forms.ValidationError('Invalid Email')
            email = email.strip()
            if User.objects.filter(email__iexact=email).exists():
                if self.instance.email:
                    if self.instance.email.lower() == email.lower():
                        pass
                    else:
                        raise forms.ValidationError('Email Already exists')
                else:
                    raise forms.ValidationError('Email Already exists')
        else:
            raise forms.ValidationError('Email is required')

        return email
