# Generated by Django 3.2.8 on 2023-09-16 20:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0008_auto_20230912_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='complainant',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
