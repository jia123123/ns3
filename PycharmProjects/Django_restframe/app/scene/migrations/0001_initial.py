# Generated by Django 2.2.4 on 2019-08-06 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SceneInfo',
            fields=[
                ('scene_id', models.AutoField(primary_key=True, serialize=False, verbose_name='场景编号')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('img', models.ImageField(upload_to='images')),
                ('desc', models.TextField(default='', verbose_name='场景描述')),
            ],
        ),
    ]
