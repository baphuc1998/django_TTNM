# Generated by Django 2.2.4 on 2019-10-11 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HTQL', '0010_auto_20191008_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studyprogram',
            name='status',
            field=models.CharField(choices=[('liked', 'liked'), ('registered', 'registered'), ('paused', 'paused')], max_length=30),
        ),
    ]
