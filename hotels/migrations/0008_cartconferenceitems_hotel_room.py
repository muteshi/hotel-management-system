# Generated by Django 3.0.2 on 2020-03-10 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0007_cartconferenceitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartconferenceitems',
            name='hotel_room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Room'),
        ),
    ]
