# Generated by Django 4.1.2 on 2022-11-28 13:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0008_customuser_two_factor_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='upload_till_now',
            field=models.IntegerField(default=0),
        ),
    ]