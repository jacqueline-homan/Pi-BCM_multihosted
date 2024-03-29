# Generated by Django 2.0.1 on 2018-01-30 04:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('customer_role', models.CharField(default='', max_length=20)),
                ('agreed', models.BooleanField(default=False)),
                ('agreed_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('agreed_version', models.CharField(default='', max_length=30, null=True)),
                ('login_count', models.IntegerField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
