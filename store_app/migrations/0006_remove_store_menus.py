# Generated by Django 2.2.4 on 2019-08-20 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0005_auto_20190820_1817'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='menus',
        ),
    ]
