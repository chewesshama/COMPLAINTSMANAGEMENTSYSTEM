# Generated by Django 4.2.5 on 2023-10-03 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0002_remove_complaintattachments_picture_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='attachments',
        ),
        migrations.RemoveField(
            model_name='remark',
            name='attachments',
        ),
        migrations.DeleteModel(
            name='ComplaintAttachments',
        ),
        migrations.AddField(
            model_name='complaint',
            name='attachments',
            field=models.FileField(blank=True, null=True, upload_to='complaint_attachments/'),
        ),
        migrations.AddField(
            model_name='remark',
            name='attachments',
            field=models.FileField(blank=True, null=True, upload_to='remark_attachments/'),
        ),
    ]