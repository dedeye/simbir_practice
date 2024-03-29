# Generated by Django 3.0.8 on 2020-07-23 10:15

from django.db import migrations, models
import django.db.models.deletion
import sortedm2m.fields


class Migration(migrations.Migration):

    replaces = [('goods_service', '0001_squashed_0003_remove_advertimage_deleted_at'), ('goods_service', '0002_advertimage_deleted'), ('goods_service', '0003_auto_20200723_0950'), ('goods_service', '0004_auto_20200723_1012')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdvertTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('contacts', models.TextField(max_length=300)),
                ('price', models.PositiveIntegerField(blank=True, null=True)),
                ('views', models.PositiveIntegerField(default=0)),
                ('tags', sortedm2m.fields.SortedManyToManyField(help_text=None, to='goods_service.AdvertTag')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='AdvertImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='img')),
                ('advert', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='image', to='goods_service.Advert')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
