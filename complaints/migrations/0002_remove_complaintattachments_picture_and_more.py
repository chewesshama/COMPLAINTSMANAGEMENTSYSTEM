# Generated by Django 4.2.5 on 2023-10-02 12:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaintattachments',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='complaintattachments',
            name='video',
        ),
        migrations.RemoveField(
            model_name='complaintattachments',
            name='voice',
        ),
        migrations.AddField(
            model_name='complaintattachments',
            name='content_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='complaintattachments',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='complaintattachments',
            name='uploaded_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='complaintattachments',
            name='uploaded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='complaintattachments',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='complaint_pictures/'),
        ),
    ]
