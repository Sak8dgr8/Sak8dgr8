# Generated by Django 4.2.2 on 2023-11-24 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0070_alter_bank_routing_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='routing_number',
            field=models.IntegerField(),
        ),
    ]
