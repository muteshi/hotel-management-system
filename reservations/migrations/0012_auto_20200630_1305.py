# Generated by Django 3.0.2 on 2020-06-30 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0011_booking_commission_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commission_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
            ],
            options={
                'verbose_name_plural': 'Booking Settings',
            },
        ),
        migrations.RemoveField(
            model_name='booking',
            name='commission_total',
        ),
    ]
