# Generated by Django 2.0.6 on 2019-04-10 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0005_auto_20190405_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotions',
            name='PromotionPrice',
            field=models.IntegerField(null=True),
        ),
    ]