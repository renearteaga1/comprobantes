# Generated by Django 2.1.5 on 2019-06-11 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cargar', '0007_auto_20190610_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='comprobante',
            name='numero_comprobante',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comprobante',
            name='conteo_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cargar.ConteoComprobante'),
        ),
    ]
