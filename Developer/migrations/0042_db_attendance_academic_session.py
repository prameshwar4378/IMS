# Generated by Django 4.1.7 on 2023-04-18 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Developer', '0041_db_attendance_student_class_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_attendance',
            name='academic_session',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
