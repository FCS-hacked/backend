# Generated by Django 4.1.2 on 2022-10-29 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_customuser_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personaluser',
            old_name='proof_of_id',
            new_name='proof_of_identity',
        ),
    ]
