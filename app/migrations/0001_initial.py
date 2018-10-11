# Generated by Django 2.0.3 on 2018-10-11 03:42

import app.models.image_upload
import app.models.task
import colorfield.fields
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('phone_number', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
                ('icon', models.ImageField(upload_to='')),
            ],
            options={
                'db_table': 'myuser',
            },
        ),
        migrations.CreateModel(
            name='ImageUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(help_text='File uploaded by a user', upload_to=app.models.image_upload.image_directory_path)),
            ],
        ),
        migrations.CreateModel(
            name='PluginDatum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, help_text='Setting key', max_length=255)),
                ('int_value', models.IntegerField(blank=True, default=None, help_text='Integer value', null=True)),
                ('float_value', models.FloatField(blank=True, default=None, help_text='Float value', null=True)),
                ('bool_value', models.NullBooleanField(default=None, help_text='Bool value')),
                ('string_value', models.TextField(blank=True, default=None, help_text='String value', null=True)),
                ('json_value', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=None, help_text='JSON value', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Preset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='A label used to describe the preset', max_length=255)),
                ('options', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=[], help_text="Options that define this preset (same format as in a Task's options).", validators=[app.models.task.validate_task_options])),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, help_text='Creation date')),
                ('system', models.BooleanField(db_index=True, default=False, help_text='Whether this preset is available to every user in the system or just to its owner.')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='A label used to describe the project', max_length=255)),
                ('description', models.TextField(blank=True, default='', help_text='More in-depth description of the project')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, help_text='Creation date')),
                ('deleting', models.BooleanField(db_index=True, default=False, help_text='Whether this project has been marked for deletion. Projects that have running tasks need to wait for tasks to be properly cleaned up before they can be deleted.')),
            ],
            options={
                'permissions': (('view_project', 'Can view project'),),
            },
        ),
        migrations.CreateModel(
            name='ProjectGroupObjectPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectUserObjectPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(help_text='The name of your application', max_length=255)),
                ('app_logo', models.ImageField(help_text='A 512x512 logo of your application (.png or .jpeg)', upload_to='settings/')),
                ('organization_name', models.CharField(blank=True, default='WebODM', help_text='The name of your organization', max_length=255, null=True)),
                ('organization_website', models.URLField(blank=True, default='https://github.com/OpenDroneMap/WebODM/', help_text='The website URL of your organization', max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('uuid', models.CharField(blank=True, db_index=True, default='', help_text="Identifier of the task (as returned by OpenDroneMap's REST API)", max_length=255)),
                ('name', models.CharField(blank=True, help_text='A label for the task', max_length=255, null=True)),
                ('processing_time', models.IntegerField(default=-1, help_text='Number of milliseconds that elapsed since the beginning of this task (-1 indicates that no information is available)')),
                ('auto_processing_node', models.BooleanField(default=True, help_text='A flag indicating whether this task should be automatically assigned a processing node')),
                ('status', models.IntegerField(blank=True, choices=[(10, 'QUEUED'), (20, 'RUNNING'), (30, 'FAILED'), (40, 'COMPLETED'), (50, 'CANCELED')], db_index=True, help_text='Current status of the task', null=True)),
                ('last_error', models.TextField(blank=True, help_text='The last processing error received', null=True)),
                ('options', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}, help_text='Options that are being used to process this task', validators=[app.models.task.validate_task_options])),
                ('available_assets', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=80), blank=True, default=[], help_text='List of available assets to download', size=None)),
                ('console_output', models.TextField(blank=True, default='', help_text="Console output of the OpenDroneMap's process")),
                ('ground_control_points', models.FileField(blank=True, help_text='Optional Ground Control Points file to use for processing', null=True, upload_to=app.models.task.gcp_directory_path)),
                ('orthophoto_extent', django.contrib.gis.db.models.fields.GeometryField(blank=True, help_text='Extent of the orthophoto created by OpenDroneMap', null=True, srid=4326)),
                ('dsm_extent', django.contrib.gis.db.models.fields.GeometryField(blank=True, help_text='Extent of the DSM created by OpenDroneMap', null=True, srid=4326)),
                ('dtm_extent', django.contrib.gis.db.models.fields.GeometryField(blank=True, help_text='Extent of the DTM created by OpenDroneMap', null=True, srid=4326)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, help_text='Creation date')),
                ('pending_action', models.IntegerField(blank=True, choices=[(1, 'CANCEL'), (2, 'REMOVE'), (3, 'RESTART'), (4, 'RESIZE')], db_index=True, help_text='A requested action to be performed on the task. The selected action will be performed by the worker at the next iteration.', null=True)),
                ('public', models.BooleanField(default=False, help_text='A flag indicating whether this task is available to the public')),
                ('resize_to', models.IntegerField(default=-1, help_text='When set to a value different than -1, indicates that the images for this task have been / will be resized to the size specified here before processing.')),
            ],
            options={
                'permissions': (('view_task', 'Can view task'),),
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of theme', max_length=255)),
                ('primary', colorfield.fields.ColorField(default='#2c3e50', help_text='Most text, icons, and borders.', max_length=18)),
                ('secondary', colorfield.fields.ColorField(default='#ffffff', help_text='The main background color, and text color of some buttons.', max_length=18)),
                ('tertiary', colorfield.fields.ColorField(default='#18bc9c', help_text='Navigation links.', max_length=18)),
                ('button_primary', colorfield.fields.ColorField(default='#2c3e50', help_text='Primary button color.', max_length=18)),
                ('button_default', colorfield.fields.ColorField(default='#95a5a6', help_text='Default button color.', max_length=18)),
                ('button_danger', colorfield.fields.ColorField(default='#e74c3c', help_text='Delete button color.', max_length=18)),
                ('header_background', colorfield.fields.ColorField(default='#18bc9c', help_text="Background color of the site's header.", max_length=18)),
                ('header_primary', colorfield.fields.ColorField(default='#ffffff', help_text="Text and icons in the site's header.", max_length=18)),
                ('border', colorfield.fields.ColorField(default='#e7e7e7', help_text='The color of most borders.', max_length=18)),
                ('highlight', colorfield.fields.ColorField(default='#f7f7f7', help_text='The background color of panels and some borders.', max_length=18)),
                ('dialog_warning', colorfield.fields.ColorField(default='#f39c12', help_text='The border color of warning dialogs.', max_length=18)),
                ('failed', colorfield.fields.ColorField(default='#ffcbcb', help_text='The background color of failed notifications.', max_length=18)),
                ('success', colorfield.fields.ColorField(default='#cbffcd', help_text='The background color of success notifications.', max_length=18)),
                ('css', models.TextField(blank=True, default='')),
                ('html_before_header', models.TextField(blank=True, default='')),
                ('html_after_header', models.TextField(blank=True, default='')),
                ('html_after_body', models.TextField(blank=True, default='')),
                ('html_footer', models.TextField(blank=True, default='')),
            ],
        ),
    ]
