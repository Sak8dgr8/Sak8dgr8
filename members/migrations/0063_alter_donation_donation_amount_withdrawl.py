# Generated by Django 4.2.2 on 2023-11-18 22:17

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0062_remove_project_project_qr_code_project_page_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='donation_amount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(50000)]),
        ),
        migrations.CreateModel(
            name='Withdrawl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('withdrawl_id', models.PositiveIntegerField(default=0)),
                ('withdrawl_title', models.CharField(max_length=100)),
                ('withdrawl_description', models.TextField(null=True)),
                ('withdrawl_amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(50000)])),
                ('withdrawl_proof', models.FileField(upload_to='proof/%y', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['.pdf', '.doc', '.docx.jpg', '.png', '.xls'])])),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawls', to='members.project')),
            ],
        ),
    ]
