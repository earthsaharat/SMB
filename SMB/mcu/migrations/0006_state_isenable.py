# Generated by Django 2.0.3 on 2018-05-31 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcu', '0005_remove_profile_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='isEnable',
            field=models.BooleanField(default=True),
        ),
    ]
