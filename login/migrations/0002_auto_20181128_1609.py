# Generated by Django 2.0.6 on 2018-11-28 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='IsActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='IsActive',
            field=models.BooleanField(default=True),
        ),
    ]
