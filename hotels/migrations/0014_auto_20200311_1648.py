# Generated by Django 3.0.2 on 2020-03-11 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0013_auto_20200311_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartconferenceitems',
            name='nights',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
