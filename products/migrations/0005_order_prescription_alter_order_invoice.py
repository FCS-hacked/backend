# Generated by Django 4.1.2 on 2022-11-25 17:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0004_document_signed_by_hospital_and_more'),
        ('products', '0004_alter_order_invoice_alter_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='prescription',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE,
                                       related_name='prescription_order', to='documents.document'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='invoice',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                       related_name='invoice_order', to='documents.document'),
        ),
    ]
