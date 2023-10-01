from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from mtaa import districts


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class ComplaintAttachments(models.Model):
    picture = models.ImageField(upload_to="complaint_pictures", null=True, blank=True)
    video = models.FileField(upload_to="complaint_videos", blank=True, null=True)
    voice = models.FileField(upload_to="complaint_voices", blank=True, null=True)
    file = models.FileField(upload_to="complaint_files", blank=True, null=True)

    def __str__(self):
        return f"{self.picture.url}"


STATUS_CHOICES = (
    ("Opened", "Opened"),
    ("Forwarded", "Forwarded"),
    ("Closed", "Closed"),
)


class User(AbstractUser):
    def validate_districts(value):
        for district in districts:
            if district["name"] == value:
                return

        raise ValidationError("The district is not known")

    departments = models.ManyToManyField(Department, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", default="default_pic.jpg", blank=True, null=True
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(
        max_length=100, blank=True, validators=[validate_districts]
    )

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class Complaint(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    complainant = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    attachments = models.ManyToManyField(ComplaintAttachments)
    targeted_department = models.ForeignKey(Department, related_name="complaint_department", on_delete=models.CASCADE)
    targeted_personnel = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="complaints_targeted"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Opened")
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    department_history = models.ManyToManyField(Department, through='DepartmentHistory', related_name="history", blank=True)

    class Meta:
        ordering = ['-date_added']

    def save(self, *args, **kwargs):
        if self.pk is not None:
            original_complaint = Complaint.objects.get(pk=self.pk)
            if self.status != original_complaint.status:
                DepartmentHistory.objects.create(
                    complaint=self,
                    department=self.targeted_department,
                    status=self.status
                )

        super(Complaint, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title},  by  {self.complainant}"


class Remark(models.Model):
    respondent = models.ForeignKey(User, on_delete=models.CASCADE)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="remarks")
    content = models.TextField()
    attachments = models.ManyToManyField(ComplaintAttachments)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Opened")
    remark_targeted_personnel = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="remark_target", default=1
    )
    remark_targeted_department = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.status == "Forwarded":
            self.complaint.targeted_department = self.remark_targeted_department
            self.complaint.status = self.status
            self.complaint.save()
        super(Remark, self).save(*args, **kwargs)

    def __str__(self):
        return f"{ self.complaint }  -  {self.content},  by  {self.respondent}"


class DepartmentHistory(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Opened")

    def __str__(self):
        return f"{self.status} ({self.department})"
