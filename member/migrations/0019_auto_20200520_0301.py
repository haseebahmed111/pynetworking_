# Generated by Django 3.0.5 on 2020-05-19 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0018_transaction_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='birth_date',
            field=models.DateField(blank=True, default='2000-12-11'),
        ),
        migrations.AlterField(
            model_name='member',
            name='cnic',
            field=models.CharField(default=0, max_length=13),
        ),
    ]
