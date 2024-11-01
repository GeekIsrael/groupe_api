# Generated by Django 5.1.2 on 2024-10-26 13:53

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gardien',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('telephone', models.CharField(max_length=15, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GroupeElectrogene',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('qr_code', models.CharField(editable=False, max_length=100)),
                ('nom', models.CharField(max_length=100)),
                ('marque', models.CharField(max_length=100)),
                ('modele', models.CharField(max_length=100)),
                ('autonomie', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
