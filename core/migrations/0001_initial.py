# Generated by Django 5.0.4 on 2024-04-03 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True)),
                ('music_genre', models.CharField(choices=[('rock', 'Rock'), ('pop', 'Pop'), ('hip_hop', 'Hip Hop'), ('country', 'Country')], max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
            ],
        ),
    ]