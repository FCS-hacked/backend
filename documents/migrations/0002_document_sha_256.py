# Generated by Django 4.1.2 on 2022-10-27 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='sha_256',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]