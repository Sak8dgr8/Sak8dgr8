# Generated by Django 4.2.2 on 2023-12-23 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0073_alter_withdrawl_withdrawl_proof'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='withdrawl',
            name='id',
        ),
        migrations.AlterField(
            model_name='withdrawl',
            name='withdrawl_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
