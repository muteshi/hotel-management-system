# Generated by Django 3.0.2 on 2020-02-27 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0002_cartpackageitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='packages',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='packages',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
