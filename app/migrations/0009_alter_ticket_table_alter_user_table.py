# Generated by Django 5.0.3 on 2024-10-28 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_ticket_table_alter_user_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='ticket',
            table='ticket',
        ),
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
    ]
