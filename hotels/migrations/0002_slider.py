# Generated by Django 3.0.2 on 2020-03-02 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='slider_photos')),
                ('header_text', models.CharField(blank=True, max_length=120, null=True)),
                ('text', models.CharField(blank=True, max_length=120, null=True)),
                ('active', models.BooleanField(default=False)),
                ('featured', models.BooleanField(default=False)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('start_Date', models.DateField(blank=True, null=True)),
                ('end_Date', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Sliders',
            },
        ),
    ]
