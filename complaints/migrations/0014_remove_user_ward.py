# Generated by Django 3.2.8 on 2023-09-17 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0013_auto_20230918_0007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='ward',
        ),
    ]
