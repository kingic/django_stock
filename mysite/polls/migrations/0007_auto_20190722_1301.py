# Generated by Django 2.2.3 on 2019-07-22 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20190722_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='industry_name',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.DeleteModel(
            name='Upjong',
        ),
    ]
