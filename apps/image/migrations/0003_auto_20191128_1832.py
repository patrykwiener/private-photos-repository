# Generated by Django 2.2.6 on 2019-11-28 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0002_auto_20191128_1424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facemodel',
            name='slug',
        ),
        migrations.AddField(
            model_name='recognizedpersonmodel',
            name='slug',
            field=models.SlugField(default='djangodbmodelsfieldscharfield', max_length=250),
        ),
    ]