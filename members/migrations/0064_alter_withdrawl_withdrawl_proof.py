# Generated by Django 4.2.2 on 2023-11-18 23:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0063_alter_donation_donation_amount_withdrawl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='withdrawl',
            name='withdrawl_proof',
            field=models.FileField(upload_to='proof/%y', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docxjpg', 'png', 'xls'])]),
        ),
    ]
