# Generated by Django 3.1.2 on 2020-10-24 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inanutshell_app', '0002_remove_files_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='docs',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
