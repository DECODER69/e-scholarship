# Generated by Django 4.1.1 on 2022-10-20 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nstpapp', '0005_alter_extenduser_end_dates_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extenduser',
            name='end_dates',
            field=models.DateField(auto_now_add=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='extenduser',
            name='start_dates',
            field=models.DateField(auto_now_add=True, verbose_name='Date'),
        ),
    ]
