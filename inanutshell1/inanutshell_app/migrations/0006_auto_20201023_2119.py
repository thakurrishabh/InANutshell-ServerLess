# Generated by Django 3.1.2 on 2020-10-24 01:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inanutshell_app', '0005_files_docs'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='files',
            name='docs',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
    ]
