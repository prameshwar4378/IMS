# Generated by Django 4.2 on 2023-05-21 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Developer', '0069_customuser_is_whats_app_sms'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='no_of_txt_sms',
            field=models.IntegerField(null=True),
        ),
    ]
