# Generated by Django 4.2.1 on 2023-06-07 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='working_days',
            field=models.ManyToManyField(blank=True, to='doctor.day'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='working_hours',
            field=models.ManyToManyField(blank=True, to='doctor.hour'),
        ),
    ]
