# Generated by Django 5.0.4 on 2024-04-29 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='numberrange',
            name='code',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='numberrange',
            name='inn',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='numberrange',
            name='territory_gar',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
