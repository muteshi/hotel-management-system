# Generated by Django 3.0.2 on 2020-03-11 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0008_conferencereservation_room_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conferencereservation',
            name='room_discount',
        ),
    ]
