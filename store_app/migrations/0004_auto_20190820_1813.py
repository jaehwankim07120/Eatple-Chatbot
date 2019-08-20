# Generated by Django 2.2.4 on 2019-08-20 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0003_auto_20190820_1809'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='store',
            new_name='stores',
        ),
        migrations.AddField(
            model_name='store',
            name='menus',
            field=models.ManyToManyField(help_text='Select a Menu for this Store', to='store_app.Menu'),
        ),
    ]
