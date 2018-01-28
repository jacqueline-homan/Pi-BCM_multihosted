# Generated by Django 2.0.1 on 2018-01-28 18:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company_organisations', '0001_initial'),
        ('member_organisations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prefix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(db_index=True, max_length=12, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_suspended', models.BooleanField(default=False)),
                ('is_special', models.CharField(default='', max_length=20)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('starting_from', models.CharField(max_length=13, null=True)),
                ('starting_from_gln', models.CharField(max_length=13, null=True)),
                ('description', models.CharField(default='', max_length=100)),
                ('company_organisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='company_organisations.CompanyOrganisation')),
                ('member_organisation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='member_organisations.MemberOrganisation')),
            ],
            options={
                'verbose_name_plural': 'prefixes',
            },
        ),
    ]
