from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import User, Department, Complaint
from django.contrib.auth.models import Group
from mtaa import tanzania



class CEORegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label="firstname",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        label="lastname",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    username = forms.CharField(
        label="username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
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
        required=True,
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
    first_name = forms.CharField(
        label="firstname",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        label="lastname",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    username = forms.CharField(
        label="username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

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
    REGION_CHOICES = [(region, region) for region in tanzania]

    first_name = forms.CharField(
        label="firstname",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        label="lastname",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    username = forms.CharField(
        label="username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    profile_picture = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    location = forms.ChoiceField(
        choices=REGION_CHOICES,
        label="location",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    
    phone_number = forms.CharField(
        label = "phone number",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

#    def __init__(self, *args, **kwargs):
#        super(UserProfileForm, self).__init__(*args, **kwargs)
#        self.fields['residence_district'] = forms.ChoiceField(
#            choices=[],
#            label="District",
#            widget=forms.Select(attrs={'class': 'form-control'}),
#        )
#        self.fields['residence_ward'] = forms.ChoiceField(
#            choices=[],
#            label="Ward",
#            widget=forms.Select(attrs={'class': 'form-control'}),
#        )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email','profile_picture', 'phone_number', 'location')


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


class AddComplaintForm(forms.ModelForm):
    title = forms.CharField(
        label="title",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    description = forms.CharField(
        label="description",
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    
    attachments = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False
    )

    targeted_personnel = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    targeted_department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        label="Department",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    STATUS_CHOICES = (
        ('Opened', 'Opened'),
        ('Forwarded', 'Forwarded'),
        ('Closed', 'Closed'),
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        label="status",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Complaint
        fields = ['title', 'description', 'attachments', 'targeted_department', 'targeted_personnel', 'status']


