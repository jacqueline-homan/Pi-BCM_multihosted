# Generated by Django 2.0.1 on 2018-01-26 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BCM', '0005_auto_20180117_1742'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ('name',), 'verbose_name_plural': 'Countries'},
        ),
    ]
