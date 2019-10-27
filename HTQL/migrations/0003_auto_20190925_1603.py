# Generated by Django 2.2.4 on 2019-09-25 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HTQL', '0002_auto_20190925_1411'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='teacher_id',
        ),
        migrations.AddField(
            model_name='subject',
            name='teacher_id',
            field=models.ManyToManyField(related_name='sub_in_teacher', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('eduprogram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HTQL.EduProgram')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]