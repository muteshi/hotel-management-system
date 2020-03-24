# Generated by Django 3.0.2 on 2020-03-10 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0006_conferenceroom_room_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartConferenceItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('line_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('CheckIn', models.DateField(blank=True, null=True)),
                ('CheckOut', models.DateField(blank=True, null=True)),
                ('stay_duration', models.PositiveIntegerField(default=1)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Cart')),
                ('rooms', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.ConferenceRoom')),
            ],
            options={
                'verbose_name_plural': 'Conference Cart Items',
            },
        ),
    ]