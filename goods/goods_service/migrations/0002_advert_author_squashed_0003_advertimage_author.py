# Generated by Django 3.1 on 2020-08-22 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('goods_service', '0002_advert_author'), ('goods_service', '0003_advertimage_author')]

    dependencies = [
        ('goods_service', '0001_squashed_0004_auto_20200723_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='advert',
            name='author',
            field=models.CharField(default='empty@user.no', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='advertimage',
            name='author',
            field=models.CharField(default='someone@none.net', max_length=100),
            preserve_default=False,
        ),
    ]
