# Generated by Django 3.0.2 on 2020-06-08 20:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hotels', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Booking Status',
            },
        ),
        migrations.CreateModel(
            name='PaymentOptions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Payment Options',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_id', models.CharField(default='ABC', max_length=120, unique=True)),
                ('sub_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('tax_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('final_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('status', models.CharField(choices=[('Started', 'Started'), ('Abandoned', 'Abandoned'), ('Finished', 'Finished')], default='Started', max_length=120)),
                ('payment_option', models.CharField(choices=[('pay_on_checkin', 'Pay on CheckIn'), ('visa_mastercard', 'Visa or MasterCard')], default='pay_on_checkin', max_length=120)),
                ('special_request', models.TextField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Cart')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Reservations',
            },
        ),
        migrations.CreateModel(
            name='PackageReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_id', models.CharField(default='ABC', max_length=120, unique=True)),
                ('sub_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('tax_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('final_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('status', models.CharField(choices=[('Started', 'Started'), ('Abandoned', 'Abandoned'), ('Finished', 'Finished')], default='Started', max_length=120)),
                ('payment_option', models.CharField(choices=[('pay_on_checkin', 'Pay on CheckIn'), ('visa_mastercard', 'Visa or MasterCard')], default='pay_on_checkin', max_length=120)),
                ('special_request', models.TextField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Cart')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Package Reservations',
            },
        ),
        migrations.CreateModel(
            name='ConferenceReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisation_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('mobile_Number', models.CharField(max_length=12)),
                ('reservation_id', models.CharField(default='ABC', max_length=120, unique=True)),
                ('start_time', models.TimeField()),
                ('attachment', models.FileField(blank=True, null=True, upload_to='pay_attachments')),
                ('final_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('name_of_guests', models.TextField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Cart')),
                ('crooms', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.ConferenceRoom')),
                ('hrooms', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Room')),
            ],
            options={
                'verbose_name_plural': 'Conference Reservations',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(blank=True, max_length=255, null=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(max_length=255)),
                ('mobile_Number', models.CharField(max_length=12)),
                ('register_as_user', models.BooleanField(default=False)),
                ('checkin', models.DateField(blank=True, null=True)),
                ('checkout', models.DateField(blank=True, null=True)),
                ('room_qty', models.PositiveIntegerField(default=1)),
                ('reservation_id', models.CharField(default='ABC', max_length=120, unique=True)),
                ('final_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('tax_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=1000)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='pay_attachments')),
                ('organisation_name', models.CharField(blank=True, max_length=255, null=True)),
                ('name_of_guests', models.TextField(blank=True, null=True)),
                ('special_requests', models.TextField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('booking_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reservations.BookingStatus')),
                ('hotel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Hotels')),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotels.Packages')),
                ('payment_option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reservations.PaymentOptions')),
                ('room', models.ManyToManyField(blank=True, to='hotels.Room')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Bookings',
            },
        ),
    ]
