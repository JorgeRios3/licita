# Generated by Django 3.2.6 on 2022-04-07 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_permiso_usuariopermisos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuariopermisos',
            old_name='user',
            new_name='usuario',
        ),
    ]
