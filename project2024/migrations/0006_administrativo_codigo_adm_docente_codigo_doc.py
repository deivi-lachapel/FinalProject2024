# Generated by Django 5.1 on 2024-11-06 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project2024', '0005_rename_contraseña_usuario_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='administrativo',
            name='codigo_adm',
            field=models.CharField(default='default_code', max_length=20, unique=True),
        ),
        migrations.AddField(
            model_name='docente',
            name='codigo_doc',
            field=models.CharField(default='default_code', max_length=20, unique=True),
        ),
    ]
