# Generated by Django 2.0.6 on 2019-04-12 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0007_promotiontierrule'),
    ]

    operations = [
        migrations.AddField(
            model_name='seasonality',
            name='BaselineSales',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
    ]
