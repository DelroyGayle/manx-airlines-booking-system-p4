# Generated by Django 3.2.23 on 2023-11-25 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_alter_transaction_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='outbound_date',
            field=models.DateField(null=True),
        ),
    ]
