# Generated by Django 5.0.2 on 2024-02-16 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_explore_options_alter_explore_author_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='explore',
            name='thread',
        ),
    ]
