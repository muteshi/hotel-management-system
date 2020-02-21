# Generated by Django 3.0.2 on 2020-01-29 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotels', '0011_auto_20200129_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='CheckIn',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='CheckOut',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='guestFirstName',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='guestLastName',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservation',
            name='hotel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hotels.Hotels'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
