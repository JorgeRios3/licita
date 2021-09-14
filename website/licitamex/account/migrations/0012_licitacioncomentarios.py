# Generated by Django 3.2.6 on 2021-09-02 02:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20210821_0200'),
    ]

    operations = [
        migrations.CreateModel(
            name='LicitacionComentarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.CharField(max_length=1000, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('licitacion_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.usuariolicitaciones')),
            ],
        ),
    ]