# Generated by Django 4.1.2 on 2022-10-26 19:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_customuser_wallet_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='name',
        ),
        migrations.RemoveField(
            model_name='personaluser',
            name='name',
        ),
        migrations.AlterField(
            model_name='organization',
            name='custom_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='organization', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='personaluser',
            name='custom_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='personal_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
