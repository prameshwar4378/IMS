# Generated by Django 4.1.7 on 2023-04-09 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Developer', '0017_db_subjects'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_result',
            name='percentage',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='db_result',
            name='result',
            field=models.CharField(max_length=100, null=True),
        ),
    ]