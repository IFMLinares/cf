# Generated by Django 3.2.7 on 2022-06-06 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='gain',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='h',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='item',
            name='l',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='item',
            name='margin',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='v',
            field=models.FloatField(),
        ),
    ]
