# Generated by Django 2.2.5 on 2021-02-25 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0002_auto_20210225_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='places',
            field=models.ManyToManyField(blank=True, related_name='lists', to='places.Place'),
        ),
    ]
