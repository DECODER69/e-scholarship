# Generated by Django 4.1.1 on 2022-10-20 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nstpapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extenduser',
            name='end_dates',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='extenduser',
            name='start_dates',
            field=models.DateTimeField(null=True),
        ),
    ]