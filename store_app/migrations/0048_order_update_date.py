# Generated by Django 2.2.4 on 2019-09-04 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0047_auto_20190904_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
