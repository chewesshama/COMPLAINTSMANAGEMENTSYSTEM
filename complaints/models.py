from django.db import models
from django.contrib.auth.models import AbstractUser, Group



class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class ComplaintAttachments(models.Model):
    picture = models.ImageField(upload_to='complaint_pictures', null=True, blank=True)
    video = models.FileField(upload_to='complaint_videos', blank=True, null=True)
    voice = models.FileField(upload_to='complaint_voices', blank=True, null=True) 
    file = models.FileField(upload_to='complaint_files', blank=True, null=True) 
    
    def __str__(self):
        return f'{self.picture.url}'
    


STATUS_CHOICES = (
        ('Opened', 'Opened'),
        ('Forwarded', 'Forwarded'),
        ('Closed', 'Closed'),
    )


class User(AbstractUser):
    departments = models.ManyToManyField(Department, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default_pic.jpg', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class Complaint(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    complainant = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    attachments = models.ManyToManyField(ComplaintAttachments)
    targeted_department = models.ForeignKey(Department, on_delete=models.CASCADE)
    targeted_personnel = models.ForeignKey(User,on_delete=models.CASCADE ,related_name='complaints_targeted')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Opened')
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title},  by  {self.complainant}'


class Remark(models.Model):
    respondent = models.ForeignKey(User, on_delete=models.CASCADE)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    content = models.TextField()
    attachments = models.ManyToManyField(ComplaintAttachments)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Opened')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{ self.complaint }  -  {self.content},  by  {self.author}'

