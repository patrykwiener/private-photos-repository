# Generated by Django 2.2.6 on 2019-12-22 14:38

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0003_sharedimagemodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemodel',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]