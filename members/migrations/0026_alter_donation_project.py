# Generated by Django 4.2.2 on 2023-07-16 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0025_alter_donation_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='members.project'),
        ),
    ]
