# Generated by Django 2.0 on 2018-01-11 12:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djinn_contenttypes.models.sharing
import markupfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
            ],
            options={
                'swappable': 'DJINN_GROUPPROFILE_MODEL',
            },
            bases=(models.Model, djinn_contenttypes.models.sharing.SharingMixin),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('interest', models.TextField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=20, null=True)),
                ('expertise', markupfield.fields.MarkupField(blank=True, null=True, rendered_field=True, verbose_name='Expertise')),
                ('expertise_markup_type', models.CharField(choices=[('', '--'), ('html', 'HTML'), ('plain', 'Plain')], default='plain', editable=False, max_length=30)),
                ('_expertise_rendered', models.TextField(editable=False, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'swappable': 'DJINN_USERPROFILE_MODEL',
            },
        ),
    ]
