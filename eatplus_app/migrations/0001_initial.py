# Generated by Django 2.2.4 on 2019-09-24 05:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import eatplus_app.model.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Category', max_length=255)),
                ('index', models.IntegerField(default=0, help_text='Category Index')),
            ],
            options={
                'ordering': ['-index'],
            },
        ),
        migrations.CreateModel(
            name='DefaultImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(help_text='Category', max_length=255)),
                ('image', models.ImageField(storage=eatplus_app.model.utils.OverwriteStorage(), upload_to=eatplus_app.model.utils.default_directory_path)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sellingTime', models.CharField(choices=[('점심', '점심'), ('저녁', '저녁')], default=('점심', '점심'), max_length=255)),
                ('name', models.CharField(default='Menu Name', help_text='Menu Name', max_length=255)),
                ('description', models.TextField(default='Description', help_text='Description')),
                ('image', models.ImageField(default='STORE_DB/images/default/menuImg.png', storage=eatplus_app.model.utils.OverwriteStorage(), upload_to=eatplus_app.model.utils.menu_directory_path)),
                ('price', models.IntegerField(default=5500, help_text='Price')),
                ('discount', models.IntegerField(default=0, help_text='Discount')),
                ('current_stock', models.IntegerField(default=0, help_text='Current Stock')),
                ('is_status', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Store Name', help_text='Store Name', max_length=255)),
                ('addr', models.CharField(default='Address', help_text='Address', max_length=255)),
                ('owner', models.CharField(default='Owner', help_text='Owner', max_length=31)),
                ('description', models.TextField(default='Store Dscription', help_text='Store Dscription')),
                ('logo', models.ImageField(default='STORE_DB/images/default/logoImg.png', storage=eatplus_app.model.utils.OverwriteStorage(), upload_to=eatplus_app.model.utils.logo_directory_path)),
                ('lunch_pickupTime_start', models.IntegerField(choices=[(0, '11:30'), (1, '11:45'), (2, '12:00'), (3, '12:15'), (4, '12:30'), (5, '12:45'), (6, '13:00'), (7, '13:15'), (8, '13:30')], default=0)),
                ('lunch_pickupTime_end', models.IntegerField(choices=[(0, '11:30'), (1, '11:45'), (2, '12:00'), (3, '12:15'), (4, '12:30'), (5, '12:45'), (6, '13:00'), (7, '13:15'), (8, '13:30')], default=8)),
                ('dinner_pickupTime_start', models.IntegerField(choices=[(0, '17:30'), (1, '18:00'), (2, '18:30'), (3, '19:00'), (4, '19:30'), (5, '20:00'), (6, '20:30'), (7, '21:00')], default=0)),
                ('dinner_pickupTime_end', models.IntegerField(choices=[(0, '17:30'), (1, '18:00'), (2, '18:30'), (3, '19:00'), (4, '19:30'), (5, '20:00'), (6, '20:30'), (7, '21:00')], default=7)),
            ],
            options={
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='User Name', max_length=31)),
                ('identifier_code', models.CharField(default='', help_text='User ID', max_length=255)),
                ('create_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Sub Category', max_length=255)),
                ('index', models.IntegerField(default=0, help_text='Sub Category Index')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eatplus_app.Category')),
            ],
            options={
                'ordering': ['-index'],
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier_code', models.CharField(default='', help_text='User ID', max_length=255)),
                ('storeInstance', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='eatplus_app.Store')),
            ],
            options={
                'ordering': ['-storeInstance__name'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('management_code', models.CharField(blank=True, help_text='Menu Magement Code', max_length=255, null=True)),
                ('pickupTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('주문 확인중', '주문 확인중'), ('주문 완료', '주문 완료'), ('픽업 준비중', '픽업 준비중'), ('픽업 가능', '픽업 가능'), ('픽업 완료', '픽업 완료'), ('주문 만료', '주문 만료'), ('주문 취소', '주문 취소')], default='주문 완료', max_length=255)),
                ('menuInstance', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='eatplus_app.Menu')),
                ('storeInstance', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='eatplus_app.Store')),
                ('userInstance', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='eatplus_app.User')),
            ],
            options={
                'ordering': ['-pickupTime'],
            },
        ),
        migrations.AddField(
            model_name='menu',
            name='categories',
            field=models.ManyToManyField(to='eatplus_app.SubCategory'),
        ),
        migrations.AddField(
            model_name='menu',
            name='storeInstance',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='eatplus_app.Store'),
        ),
    ]
