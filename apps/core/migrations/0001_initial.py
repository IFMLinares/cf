# Generated by Django 3.2.7 on 2022-06-03 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku_code', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('image', models.ImageField(upload_to='media')),
                ('stock', models.IntegerField(default=1)),
                ('l', models.CharField(max_length=100)),
                ('h', models.CharField(max_length=100)),
                ('v', models.CharField(max_length=100)),
                ('cubic_meter', models.CharField(blank=True, max_length=100, null=True)),
                ('price_before_taxes', models.FloatField()),
                ('freight', models.FloatField()),
                ('custom_taxe', models.FloatField()),
                ('price', models.FloatField(blank=True, null=True)),
                ('sale_price', models.FloatField(blank=True, null=True)),
                ('margin', models.CharField(max_length=100)),
                ('gain', models.CharField(max_length=100)),
            ],
        ),
    ]