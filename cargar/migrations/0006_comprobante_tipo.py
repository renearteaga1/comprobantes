# Generated by Django 2.1.5 on 2019-06-10 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargar', '0005_comprobante_conteo_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='comprobante',
            name='tipo',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
