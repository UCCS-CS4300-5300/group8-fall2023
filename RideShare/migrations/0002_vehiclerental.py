# Generated by Django 3.2.13 on 2023-11-13 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RideShare', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleRental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checkoutTime', models.DateTimeField(auto_now_add=True)),
                ('checkinTime', models.DateTimeField(blank=True, null=True)),
                ('checkinLocal', models.CharField(blank=True, choices=[('Location1', 'Location 1'), ('Location2', 'Location 2'), ('Location3', 'Location 3'), ('Location4', 'Location 4'), ('Location5', 'Location 5')], max_length=200, null=True)),
                ('paymentMethod', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RideShare.vehicle')),
            ],
        ),
    ]