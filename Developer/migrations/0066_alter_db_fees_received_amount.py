# Generated by Django 4.1.7 on 2023-04-27 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Developer', '0065_alter_db_fees_received_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='db_fees',
            name='received_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
