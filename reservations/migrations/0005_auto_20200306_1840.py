# Generated by Django 3.0.2 on 2020-03-06 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0004_booking_register'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='register',
            new_name='register_as_user',
        ),
    ]
