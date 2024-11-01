# Generated by Django 5.1.2 on 2024-10-26 17:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_action_gardien'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action',
            name='gardien',
        ),
        migrations.AddField(
            model_name='action',
            name='gardien_off',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actions_extinction', to='api.gardien', verbose_name='Gardien qui a éteint'),
        ),
        migrations.AddField(
            model_name='action',
            name='gardien_on',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='actions_allumage', to='api.gardien', verbose_name='Gardien qui a allumé'),
        ),
    ]
