# Generated by Django 4.1.7 on 2023-04-06 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Developer', '0004_rename_admition_to_customuser_student_class_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_fees',
            name='pay_remark',
            field=models.CharField(choices=[('1st Standerd', '1st Standerd'), ('2nd Standerd', '2nd Standerd'), ('3rd Standerd', '3rd Standerd'), ('4th Standerd', '4th Standerd'), ('6th Standerd', '6th Standerd'), ('7th Standerd', '7th Standerd'), ('8th Standerd', '8th Standerd'), ('9th Standerd', '9th Standerd'), ('10th Standerd', '10th Standerd'), ('11th Standerd', '11th Standerd'), ('12th Standerd', '12th Standerd')], max_length=250, null=True),
        ),
    ]
