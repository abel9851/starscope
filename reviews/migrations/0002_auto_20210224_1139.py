# Generated by Django 2.2.5 on 2021-02-24 02:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='room',
            new_name='place',
        ),
    ]
