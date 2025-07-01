from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterForm(forms.ModelForm):

    confirm_password = forms.CharField(max_length=200, widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email'
        )
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Password'
            }),        
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email'
            })
        }

    def save(self, commit = ...):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('confirm password must match password')
        return super().clean()


class LoginForm(forms.Form):

    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'Username'
    }))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={
        'placeholder': 'Password'
    }))