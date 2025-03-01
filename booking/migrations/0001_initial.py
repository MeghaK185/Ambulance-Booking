# Generated by Django 5.1.2 on 2025-01-22 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AmbulanceBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('number', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=255)),
                ('textarea_message', models.TextField(blank=True, null=True)),
                ('status', models.CharField(default='Pending', max_length=20)),
            ],
        ),
    ]
