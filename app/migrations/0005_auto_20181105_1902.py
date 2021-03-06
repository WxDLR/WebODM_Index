# Generated by Django 2.0.3 on 2018-11-05 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20181022_1842'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='projectgroupobjectpermission',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='projectgroupobjectpermission',
            name='content_object',
        ),
        migrations.RemoveField(
            model_name='projectgroupobjectpermission',
            name='group',
        ),
        migrations.RemoveField(
            model_name='projectgroupobjectpermission',
            name='permission',
        ),
        migrations.AlterUniqueTogether(
            name='projectuserobjectpermission',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='projectuserobjectpermission',
            name='content_object',
        ),
        migrations.RemoveField(
            model_name='projectuserobjectpermission',
            name='permission',
        ),
        migrations.RemoveField(
            model_name='projectuserobjectpermission',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'verbose_name': '任务', 'verbose_name_plural': '任务'},
        ),
        migrations.AddField(
            model_name='project',
            name='cover',
            field=models.ImageField(default='/static/app/img/logo512.png', upload_to=''),
        ),
        migrations.DeleteModel(
            name='ProjectGroupObjectPermission',
        ),
        migrations.DeleteModel(
            name='ProjectUserObjectPermission',
        ),
    ]
