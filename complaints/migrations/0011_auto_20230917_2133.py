# Generated by Django 3.2.8 on 2023-09-17 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('complaints', '0010_auto_20230916_2359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ward',
            name='district',
        ),
        migrations.RemoveField(
            model_name='user',
            name='district',
        ),
        migrations.RemoveField(
            model_name='user',
            name='ward',
        ),
        migrations.DeleteModel(
            name='District',
        ),
        migrations.DeleteModel(
            name='Region',
        ),
        migrations.DeleteModel(
            name='Ward',
        ),
    ]
