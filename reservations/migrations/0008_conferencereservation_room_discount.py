# Generated by Django 3.0.2 on 2020-03-11 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0007_auto_20200311_1238'),
    ]

    operations = [
        migrations.AddField(
            model_name='conferencereservation',
            name='room_discount',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=1000),
        ),
    ]
