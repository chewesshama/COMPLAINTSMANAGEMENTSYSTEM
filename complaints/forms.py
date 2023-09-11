from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import User, Department
from django.contrib.auth.models import Group



class CEORegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        label="Department",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Position",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'group', 'department', 'password1', 'password2']


class HODRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    username.label = "Username"
    username.label_classes = ['text-danger']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email','profile_picture', 'phone_number')


class UserSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

class PasswordChangeCustomForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="old Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']





