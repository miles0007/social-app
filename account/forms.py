from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import Profile

class LoginForm(forms.Form):
	username = forms.CharField(label="Username / Email")
	password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password',
                               widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username','email')

    #check password and password2 matches
    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Both Password Doesn\'t match')
        return cd['password2']
    #check email exists or not
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Sorry Email already exists')
        return email

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email','first_name','last_name')

class ProfileEditForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'YYYY - MM - DD'}))
    class Meta:
        model = Profile
        fields = ('birth_date','photo')
