# Generated by Django 4.2.5 on 2023-11-19 03:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RideShare', '0005_vehicle_cost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehiclerental',
            name='paymentMethod',
        ),
        migrations.DeleteModel(
            name='UserBillingAccount',
        ),
    ]
