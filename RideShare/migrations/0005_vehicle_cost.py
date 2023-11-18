# Generated by Django 3.2.13 on 2023-11-18 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RideShare', '0004_userbillingaccount'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=5.0, max_digits=10),
        ),
    ]
