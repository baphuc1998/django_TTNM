# Generated by Django 2.2.4 on 2019-09-25 09:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HTQL', '0004_course_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='name',
        ),
        migrations.RemoveField(
            model_name='department',
            name='teacher',
        ),
        migrations.AddField(
            model_name='department',
            name='teacher',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
