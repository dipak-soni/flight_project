# Generated by Django 5.0.3 on 2024-11-05 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='aiport_code',
        ),
    ]