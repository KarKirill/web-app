# Generated by Django 5.1.3 on 2025-01-07 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blank', '0002_filesave'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinic',
            name='passport',
            field=models.TextField(default=0, verbose_name='Серия и номер паспорта'),
            preserve_default=False,
        ),
    ]
