# Generated by Django 5.1.7 on 2025-03-20 22:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipamentos', '0008_remove_intervencao_data_intervencao_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='intervencao',
            name='apagado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='intervencao',
            name='tecnico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
