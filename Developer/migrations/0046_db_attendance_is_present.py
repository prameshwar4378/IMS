# Generated by Django 4.1.7 on 2023-04-19 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Developer', '0045_customuser_date_time_db_attendance_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_attendance',
            name='is_present',
            field=models.BooleanField(default=False),
        ),
    ]
