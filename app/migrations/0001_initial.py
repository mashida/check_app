# Generated by Django 5.0.4 on 2024-04-29 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NumberRange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_number', models.IntegerField()),
                ('to_number', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('operator', models.CharField(max_length=255)),
                ('region', models.CharField(max_length=255)),
            ],
        ),
    ]
