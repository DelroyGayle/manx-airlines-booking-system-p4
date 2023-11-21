# Generated by Django 3.2.23 on 2023-11-21 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_auto_20231118_0958'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='number_of_pax',
            new_name='number_of_adults',
        ),
        migrations.AddField(
            model_name='booking',
            name='number_of_children',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
