# Generated by Django 3.0.8 on 2020-07-18 23:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods_service', '0002_auto_20200718_2312'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advert',
            options={'ordering': ['id']},
        ),
    ]
