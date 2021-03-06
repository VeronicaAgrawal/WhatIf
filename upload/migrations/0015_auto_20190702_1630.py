# Generated by Django 2.0.6 on 2019-07-02 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0014_products_brand'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProductId', models.IntegerField()),
                ('UserId', models.IntegerField()),
                ('Role', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('ShelfLife', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('AvgPurchaseFreq', models.CharField(blank=True, default=None, max_length=30, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='producthistory',
            name='BrandPresent',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='CannibalizationIds',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='CompetitorBrandIds',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='products',
            name='HaloEffectIds',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='promotions',
            name='PullForward',
            field=models.CharField(blank=True, default=None, max_length=30, null=True),
        ),
    ]
