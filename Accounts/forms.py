from django import forms
from  django.contrib.auth import get_user_model
User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


    # def clean(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    #





class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError('username taken !')
        return  username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('email exist !')
        return email

    def clean(self):
        data = self.cleaned_data
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('passwords must matches !')
        return data


