# Generated by Django 2.2.4 on 2019-08-19 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eatplus_chatbot_app', '0012_store_json_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='json_data',
        ),
        migrations.RemoveField(
            model_name='store',
            name='store_menu',
        ),
    ]
