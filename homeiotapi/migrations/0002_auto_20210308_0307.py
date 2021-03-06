# Generated by Django 3.1.7 on 2021-03-08 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeiotapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='sesnor_type',
            new_name='sensor_type',
        ),
        migrations.AlterField(
            model_name='device',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
    ]
