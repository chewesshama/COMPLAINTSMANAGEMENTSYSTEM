# Generated by Django 3.2.8 on 2023-09-28 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0018_alter_complaint_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remark',
            name='complaint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='remarks', to='complaints.complaint'),
        ),
    ]