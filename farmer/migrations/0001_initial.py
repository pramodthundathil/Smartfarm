# Generated by Django 3.2.14 on 2023-02-24 02:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SeedFarm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seedname', models.CharField(max_length=55)),
                ('farmfield', models.CharField(max_length=55)),
                ('framarea', models.CharField(max_length=55)),
                ('framstatus', models.CharField(max_length=1000)),
                ('image', models.FileField(upload_to='framimage')),
                ('date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
