# Generated by Django 4.1.1 on 2022-10-20 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nstpapp', '0004_alter_extenduser_end_dates_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extenduser',
            name='end_dates',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='extenduser',
            name='start_dates',
            field=models.DateField(),
        ),
    ]