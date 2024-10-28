# Generated by Django 5.1.2 on 2024-10-26 16:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_gardien_groupe_associe_alter_gardien_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='gardien',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='api.gardien'),
        ),
    ]