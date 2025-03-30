# Generated by Django 5.0.7 on 2025-03-25 15:07

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('amount', models.FloatField()),
            ],
            options={
                'ordering': ('description',),
            },
        ),
    ]
