# Generated by Django 3.0.8 on 2020-07-19 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods_service', '0013_auto_20200719_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertimage',
            name='file',
            field=models.FileField(upload_to='img'),
        ),
    ]
