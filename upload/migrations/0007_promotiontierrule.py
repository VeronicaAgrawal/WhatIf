# Generated by Django 2.0.6 on 2019-04-10 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0006_promotions_promotionprice'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromotionTierRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PromotionIndexTier', models.IntegerField()),
                ('PromotionPercentage', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('PromotionType', models.CharField(default='', max_length=250)),
                ('ImpactPercentValue', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('CreatedDate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]