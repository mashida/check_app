# Generated by Django 5.0.4 on 2024-04-29 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_numberrange_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numberrange',
            name='territory_gar',
            field=models.CharField(blank=True, null=True),
        ),
    ]
