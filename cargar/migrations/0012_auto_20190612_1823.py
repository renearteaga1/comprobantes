# Generated by Django 2.1.5 on 2019-06-12 23:23

import cargar.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cargar', '0011_oficio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comprobante',
            old_name='comprobante',
            new_name='archivo',
        ),
        migrations.RemoveField(
            model_name='oficio',
            name='oficio',
        ),
        migrations.AddField(
            model_name='oficio',
            name='archivo',
            field=models.FileField(default=1, upload_to=cargar.models.oficio_directory_path),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='oficio',
            name='entrantes',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='oficio',
            name='respuesta',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
