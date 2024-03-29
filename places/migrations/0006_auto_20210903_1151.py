# Generated by Django 2.2.5 on 2021-09-03 02:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_auto_20210225_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='caption',
            field=models.CharField(max_length=80, verbose_name='caption'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(upload_to='place_photos', verbose_name='file'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='places.Place', verbose_name='place'),
        ),
        migrations.AlterField(
            model_name='place',
            name='address',
            field=models.CharField(max_length=140, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='place',
            name='city',
            field=models.CharField(max_length=80, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='place',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, verbose_name='country'),
        ),
        migrations.AlterField(
            model_name='place',
            name='description',
            field=models.TextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='place',
            name='name',
            field=models.CharField(max_length=140, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='place',
            name='viewfinder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='places', to=settings.AUTH_USER_MODEL, verbose_name='viewfinder'),
        ),
    ]
