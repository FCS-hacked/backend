# Generated by Django 4.1.2 on 2022-11-26 14:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0004_document_signed_by_hospital_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DocumentVerificationRequest',
        ),
    ]
