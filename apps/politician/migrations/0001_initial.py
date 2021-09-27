# Generated by Django 3.2.4 on 2021-09-27 02:03

import core.models
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
            name='Claim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=256)),
                ('source', models.URLField()),
                ('type', core.models.BitFlagField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Politician',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256)),
                ('current_position', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'politician_politicians',
            },
        ),
        migrations.CreateModel(
            name='FactCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('claim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='politician.claim')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='claim',
            name='politician',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='politician.politician'),
        ),
    ]
