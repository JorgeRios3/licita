# Generated by Django 3.2.6 on 2021-09-06 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_auto_20210906_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariofiltros',
            name='articulo',
            field=models.CharField(default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='usuariofiltros',
            name='familia',
            field=models.CharField(default='', max_length=250, null=True),
        ),
    ]