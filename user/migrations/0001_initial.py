# Generated by Django 2.0.1 on 2018-01-16 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(default='', max_length=255, unique=True)),
                ('username', models.CharField(default='', max_length=50, unique=True)),
                ('password', models.CharField(default='', max_length=255)),
                ('first_name', models.CharField(default='', max_length=30)),
                ('last_name', models.CharField(default='', max_length=30)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
