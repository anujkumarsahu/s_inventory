# Generated by Django 4.2.1 on 2023-10-17 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventry_app', '0007_alter_temsale_invoice_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='datetime',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='temppurchase',
            name='datetime',
            field=models.DateField(),
        ),
    ]
