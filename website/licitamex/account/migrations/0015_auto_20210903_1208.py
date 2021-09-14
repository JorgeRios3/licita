# Generated by Django 3.2.6 on 2021-09-03 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('account', '0014_usuariolicitaciones_datos_comprador'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('admin_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('company', models.CharField(blank=True, max_length=50, null=True)),
                ('subscription_id', models.CharField(blank=True, max_length=50, null=True)),
                ('plan_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]