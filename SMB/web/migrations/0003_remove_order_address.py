# Generated by Django 2.0.7 on 2018-08-01 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20180513_2138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
    ]
