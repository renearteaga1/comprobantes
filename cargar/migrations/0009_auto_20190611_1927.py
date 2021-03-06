# Generated by Django 2.1.5 on 2019-06-12 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cargar', '0008_auto_20190611_1104'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorCarga',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.CharField(blank=True, max_length=255, null=True)),
                ('tipo_error', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='conteocomprobante',
            name='errores',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='errorcarga',
            name='conteo_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cargar.ConteoComprobante'),
        ),
    ]
