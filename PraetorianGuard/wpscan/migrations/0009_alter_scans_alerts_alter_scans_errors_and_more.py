# Generated by Django 4.1.3 on 2022-12-12 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wpscan', '0008_remove_scans_data_scans_alerts_scans_errors_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scans',
            name='alerts',
            field=models.CharField(blank=True, max_length=14000),
        ),
        migrations.AlterField(
            model_name='scans',
            name='errors',
            field=models.CharField(blank=True, max_length=14000),
        ),
        migrations.AlterField(
            model_name='scans',
            name='finds',
            field=models.CharField(blank=True, max_length=14000),
        ),
        migrations.AlterField(
            model_name='scans',
            name='info',
            field=models.CharField(blank=True, max_length=14000),
        ),
        migrations.AlterField(
            model_name='scans',
            name='resu',
            field=models.CharField(blank=True, max_length=14000),
        ),
        migrations.AlterField(
            model_name='scans',
            name='sum',
            field=models.CharField(blank=True, max_length=14000),
        ),
        migrations.AlterField(
            model_name='scans',
            name='sum_line',
            field=models.CharField(blank=True, max_length=14000),
        ),
        migrations.AlterField(
            model_name='scans',
            name='warns',
            field=models.CharField(blank=True, max_length=14000),
        ),
    ]