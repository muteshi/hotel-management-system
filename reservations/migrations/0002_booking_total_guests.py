# Generated by Django 3.0.2 on 2020-06-12 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='total_guests',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
