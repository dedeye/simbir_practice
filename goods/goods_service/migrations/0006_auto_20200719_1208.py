# Generated by Django 3.0.8 on 2020-07-19 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods_service', '0005_advertimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertimage',
            name='advert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='goods_service.Advert'),
        ),
    ]
