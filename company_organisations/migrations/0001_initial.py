# Generated by Django 2.0.1 on 2018-01-30 00:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import organizations.base
import organizations.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('BCM', '0001_initial'),
        ('member_organisations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyOrganisation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The name of the organization', max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('created', organizations.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', organizations.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('slug', organizations.fields.SlugField(blank=True, editable=False, help_text='The name in all lowercase, suitable for URL identification', max_length=200, populate_from='name', unique=True)),
                ('uuid', models.CharField(max_length=50, unique=True)),
                ('company', models.CharField(default='', max_length=100)),
                ('street1', models.CharField(default='', max_length=100)),
                ('street2', models.CharField(default='', max_length=100)),
                ('city', models.CharField(default='', max_length=50)),
                ('state', models.CharField(default='', max_length=50)),
                ('zip', models.CharField(default='', max_length=20)),
                ('phone', models.CharField(default='', max_length=20)),
                ('gln', models.CharField(default='', max_length=13)),
                ('vat', models.CharField(default='', max_length=12)),
                ('credit_points_balance', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=True)),
                ('prefix_override', models.CharField(default='', max_length=100)),
                ('country', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='BCM.Country')),
                ('member_organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companies', to='member_organisations.MemberOrganisation')),
            ],
            options={
                'verbose_name': 'organization',
                'abstract': False,
                'ordering': ['name'],
                'verbose_name_plural': 'organizations',
            },
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CompanyOrganisationOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', organizations.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', organizations.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('organization', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='company_organisations.CompanyOrganisation')),
            ],
            options={
                'verbose_name': 'organization owner',
                'abstract': False,
                'verbose_name_plural': 'organization owners',
            },
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CompanyOrganisationUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', organizations.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', organizations.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_users', to='company_organisations.CompanyOrganisation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_organisations_companyorganisationuser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'ordering': ['organization', 'user'],
                'verbose_name': 'organization user',
                'verbose_name_plural': 'organization users',
            },
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.AddField(
            model_name='companyorganisationowner',
            name='organization_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='company_organisations.CompanyOrganisationUser'),
        ),
        migrations.AddField(
            model_name='companyorganisation',
            name='users',
            field=models.ManyToManyField(related_name='company_organisations_companyorganisation', through='company_organisations.CompanyOrganisationUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='companyorganisationuser',
            unique_together={('user', 'organization')},
        ),
    ]
