# Generated by Django 3.0.5 on 2020-04-28 21:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0012_auto_20200429_0201'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='account',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='member.Account'),
        ),
        migrations.AddField(
            model_name='member',
            name='membership',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='member.Membership'),
        ),
        migrations.AddField(
            model_name='member',
            name='referral',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='member.Referral'),
        ),
    ]
