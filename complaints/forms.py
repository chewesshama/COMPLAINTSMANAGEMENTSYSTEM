from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
)
from .models import Remark, User, Department, Complaint
from django.contrib.auth.models import Group
from mtaa import tanzania, districts


class CEORegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label="firstname", widget=forms.TextInput
    )

    last_name = forms.CharField(
        label="lastname", widget=forms.TextInput
    )

    username = forms.CharField(
        label="username", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        label="email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        label="Department",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Position",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "group",
            "department",
            "password1",
            "password2",
        ]


class HODRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label="firstname", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        label="lastname", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    username = forms.CharField(
        label="username", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        label="email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    username.label = "Username"
    username.label_classes = ["text-danger"]


class UserProfileForm(forms.ModelForm):
    REGION_CHOICES = [(region, region) for region in tanzania]

    first_name = forms.CharField(
        label="firstname", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        label="lastname", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    username = forms.CharField(
        label="username", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        label="email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    profile_picture = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    region = forms.ChoiceField(
        label="Region",
        choices=[(region, region) for region in tanzania],
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    district = forms.ChoiceField(
        label="District",
        choices=[(district, district) for district in districts],
        validators=[],
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields["region"].choices = [("", "Select a Region")] + [
            (region, region) for region in tanzania
        ]

        if "instance" in kwargs and kwargs["instance"]:
            instance = kwargs["instance"]
            if instance.region:
                selected_region = instance.region
                if hasattr(tanzania, selected_region):
                    region = getattr(tanzania, selected_region)
                    if hasattr(region, "districts"):
                        districts = [
                            (district, district) for district in region.districts
                        ]
                        self.fields["district"].choices = [
                            ("", "Select a District")
                        ] + districts

    phone_number = forms.CharField(
        label="phone number", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "profile_picture",
            "phone_number",
            "region",
            "district",
        )


class SearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )


class PasswordChangeCustomForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="old Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]


class MultiFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", forms.ClearableFileInput(attrs={"multiple": True}))
        super().__init__(*args, **kwargs)


class AddComplaintForm(forms.ModelForm):
    title = forms.CharField(
        label="title", 
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    description = forms.CharField(
        label="description",
        widget=forms.Textarea(attrs={"class": "form-control"}),
    )

    ATTACHMENT_CHOICES = [
        ("picture", "Picture"),
        ("voice", "Voice"),
        ("video", "Video"),
        ("file", "File"),
        ("all", "All"),
    ]

    attachment_type = forms.ChoiceField(
        choices=ATTACHMENT_CHOICES,
        label="Attachment Type",
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    attachments = MultiFileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={"multiple": True, "class": "form-control"}
        ),
    )

    targeted_personnel = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    targeted_department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        label="Department",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    STATUS_CHOICES = (
        ("Opened", "Opened"),
        ("Forwarded", "Forwarded"),
        ("Closed", "Closed"),
    )

    class Meta:
        model = Complaint
        fields = [
            "title",
            "description",
            "attachment_type",
            "attachments",
            "targeted_department",
            "targeted_personnel"
        ]


class AddRemarkForm(forms.ModelForm):
    complaint = forms.ModelChoiceField(
        queryset=Complaint.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    content = forms.CharField(
        label="description", widget=forms.Textarea(attrs={"class": "form-control"})
    )

    ATTACHMENT_CHOICES = [
        ("picture", "Picture"),
        ("voice", "Voice"),
        ("video", "Video"),
        ("file", "File"),
        ("all", "All"),
    ]

    attachment_type = forms.ChoiceField(
        choices=ATTACHMENT_CHOICES,
        label="Attachment Type",
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    attachments = MultiFileField(
        required=False,
        widget=forms.ClearableFileInput(
            attrs={"multiple": True, "class": "form-control"}
        ),
    )

    remark_targeted_personnel = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Forward / respond to",
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    remark_targeted_department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        label="Department",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    STATUS_CHOICES = (
        ("Forwarded", "Forwarded"),
        ("Closed", "Closed"),
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        label="status",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Remark
        fields = [
            "complaint",
            "content",
            "attachment_type",
            "attachments",
            "remark_targeted_department",
            "remark_targeted_personnel",
            "status",
        ]
