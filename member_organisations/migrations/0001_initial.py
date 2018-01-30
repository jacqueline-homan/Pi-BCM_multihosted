# Generated by Django 2.0.1 on 2018-01-30 01:57

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
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberOrganisation',
            fields=[
                ('name', models.CharField(help_text='The name of the organization', max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('created', organizations.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', organizations.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('slug', organizations.fields.SlugField(blank=True, editable=False, help_text='The name in all lowercase, suitable for URL identification', max_length=200, populate_from='name', unique=True)),
                ('country', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='member_organisation', serialize=False, to='BCM.Country')),
            ],
            options={
                'abstract': False,
                'ordering': ['name'],
                'verbose_name': 'organization',
                'verbose_name_plural': 'organizations',
            },
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MemberOrganisationOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', organizations.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', organizations.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('organization', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='member_organisations.MemberOrganisation')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'organization owner',
                'verbose_name_plural': 'organization owners',
            },
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.CreateModel(
            name='MemberOrganisationUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', organizations.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('modified', organizations.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_users', to='member_organisations.MemberOrganisation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_organisations_memberorganisationuser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['organization', 'user'],
                'verbose_name': 'organization user',
                'abstract': False,
                'verbose_name_plural': 'organization users',
            },
            bases=(organizations.base.UnicodeMixin, models.Model),
        ),
        migrations.AddField(
            model_name='memberorganisationowner',
            name='organization_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='member_organisations.MemberOrganisationUser'),
        ),
        migrations.AddField(
            model_name='memberorganisation',
            name='users',
            field=models.ManyToManyField(related_name='member_organisations_memberorganisation', through='member_organisations.MemberOrganisationUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='memberorganisationuser',
            unique_together={('user', 'organization')},
        ),
    ]
