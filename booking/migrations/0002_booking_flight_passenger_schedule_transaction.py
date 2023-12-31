# Generated by Django 3.2.23 on 2023-11-23 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pnr', models.CharField(max_length=6, unique=True)),
                ('created_at', models.DateField(auto_now=True)),
                ('amended_at', models.DateField(auto_now_add=True)),
                ('flight_from', models.CharField(max_length=3)),
                ('flight_to', models.CharField(max_length=3)),
                ('return_flight', models.BooleanField(default=True)),
                ('outbound_date', models.DateField(auto_now=True)),
                ('outbound_flightno', models.CharField(default='', max_length=6)),
                ('inbound_date', models.DateField(null=True)),
                ('inbound_flightno', models.CharField(blank=True, default='', max_length=6)),
                ('fare_quote', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('ticket_class', models.CharField(default='Y', max_length=1)),
                ('cabin_class', models.CharField(default='Y', max_length=1)),
                ('number_of_adults', models.PositiveSmallIntegerField(default=0)),
                ('number_of_children', models.PositiveSmallIntegerField(default=0)),
                ('number_of_infants', models.PositiveSmallIntegerField(default=0)),
                ('number_of_bags', models.PositiveSmallIntegerField(default=0)),
                ('departure_time', models.CharField(max_length=4)),
                ('arrival_time', models.CharField(max_length=4)),
                ('remarks', models.TextField(blank=True, default='')),
            ],
            options={
                'ordering': ['pnr'],
            },
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('flight_number', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('flight_from', models.CharField(max_length=3)),
                ('flight_to', models.CharField(max_length=3)),
                ('flight_STD', models.CharField(max_length=4)),
                ('flight_STA', models.CharField(max_length=4)),
                ('outbound', models.BooleanField(default=True)),
                ('capacity', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ['flight_number'],
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_date', models.DateField()),
                ('flight_number', models.CharField(max_length=6)),
                ('total_booked', models.PositiveSmallIntegerField()),
                ('seatmap', models.CharField(default='000000000000', max_length=12)),
            ],
            options={
                'ordering': ['flight_date', 'flight_number'],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pnr', models.CharField(max_length=6)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('date_created', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=4)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('pax_type', models.CharField(default='A', max_length=1)),
                ('pax_number', models.PositiveSmallIntegerField(default=1)),
                ('date_of_birth', models.DateField(null=True)),
                ('contact_number', models.CharField(blank=True, default='', max_length=40)),
                ('contact_email', models.CharField(blank=True, default='', max_length=40)),
                ('seat_number', models.PositiveSmallIntegerField(default=0)),
                ('status', models.CharField(max_length=4)),
                ('wheelchair_ssr', models.CharField(blank=True, default='', max_length=1)),
                ('wheelchair_type', models.CharField(blank=True, default='', max_length=1)),
                ('pnr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.booking')),
            ],
        ),
    ]
