# Generated by Django 3.0.8 on 2020-07-19 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods_service', '0008_auto_20200719_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertimage',
            name='file',
            field=models.FileField(upload_to='static/'),
        ),
    ]
