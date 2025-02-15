# Generated by Django 5.1.5 on 2025-02-02 12:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Event_Name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('Date_and_Time', models.DateTimeField(blank=True, null=True)),
                ('location', models.CharField(default='Dhaka', max_length=100)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cat', to='events.category')),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Participant_Name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('event', models.ManyToManyField(related_name='event', to='events.event')),
            ],
        ),
    ]
