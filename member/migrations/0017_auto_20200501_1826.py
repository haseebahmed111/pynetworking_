# Generated by Django 3.0.5 on 2020-05-01 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0016_auto_20200501_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='contactus',
            name='phone_number',
            field=models.CharField(max_length=11),
        ),
    ]
