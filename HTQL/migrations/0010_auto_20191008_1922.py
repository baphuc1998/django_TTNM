# Generated by Django 2.2.4 on 2019-10-08 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HTQL', '0009_auto_20191008_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sub_score',
            name='score',
            field=models.FloatField(null=True),
        ),
    ]