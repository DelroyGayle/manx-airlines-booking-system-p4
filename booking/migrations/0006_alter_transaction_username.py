# Generated by Django 3.2.23 on 2023-11-25 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_auto_20231125_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='username',
            field=models.CharField(default='user', max_length=40),
        ),
    ]