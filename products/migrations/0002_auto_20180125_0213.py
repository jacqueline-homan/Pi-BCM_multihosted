# Generated by Django 2.0.1 on 2018-01-25 02:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='user',
            new_name='owner',
        ),
    ]
