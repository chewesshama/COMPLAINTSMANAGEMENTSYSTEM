# Generated by Django 3.2.8 on 2023-09-11 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0006_user_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='departments',
            field=models.ManyToManyField(blank=True, to='complaints.Department'),
        ),
    ]