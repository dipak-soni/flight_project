# Generated by Django 5.0.3 on 2024-10-25 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
