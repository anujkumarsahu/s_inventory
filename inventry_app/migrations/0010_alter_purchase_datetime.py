# Generated by Django 4.2.1 on 2023-10-17 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventry_app', '0009_alter_purchase_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='datetime',
            field=models.DateField(),
        ),
    ]
