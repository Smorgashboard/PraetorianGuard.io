# Generated by Django 4.1.3 on 2022-12-12 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wpscan', '0009_alter_scans_alerts_alter_scans_errors_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scans',
            name='vulns',
            field=models.CharField(blank=True, max_length=14000),
        ),
    ]
