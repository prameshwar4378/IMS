# Generated by Django 4.1.7 on 2023-04-06 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Developer', '0007_rename_pay_date_db_fees_received_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='db_fees',
            old_name='amount',
            new_name='received_amount',
        ),
    ]
