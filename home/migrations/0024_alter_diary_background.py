# Generated by Django 5.0.2 on 2024-02-22 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_alter_diary_background_alter_diary_weather'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diary',
            name='background',
            field=models.CharField(blank=True, choices=[('default', '默认'), ('milktea', '奶茶'), ('cat', '猫猫'), ('dragon', '龙龙'), ('dish', '吃饭')], max_length=100, null=True),
        ),
    ]
