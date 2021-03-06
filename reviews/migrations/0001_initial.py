# Generated by Django 2.2.5 on 2021-02-24 02:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('places', '0002_photo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('review', models.TextField(verbose_name='レビュー')),
                ('accuracy', models.IntegerField(verbose_name='正確性')),
                ('location', models.IntegerField(verbose_name='位置')),
                ('cleanliness', models.IntegerField(verbose_name='淸潔')),
                ('satisfaction', models.IntegerField(verbose_name='満足度')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.Place')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
