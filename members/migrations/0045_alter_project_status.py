# Generated by Django 4.2.2 on 2023-07-29 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0044_alter_project_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('nonee', 'None'), ('draft', 'Draft'), ('live', 'Live'), ('funds_withdrawn', 'Funds Withdrawn'), ('completed', 'Completed')], default='nonee', max_length=20),
        ),
    ]
