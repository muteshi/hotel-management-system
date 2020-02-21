# Generated by Django 3.0.2 on 2020-01-27 15:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0005_reservation_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='totalPrice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
    ]
