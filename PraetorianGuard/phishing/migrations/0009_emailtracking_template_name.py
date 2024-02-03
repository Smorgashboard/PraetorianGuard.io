# Generated by Django 4.1.3 on 2022-11-28 17:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('phishing', '0008_campaigns_template_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailtracking',
            name='template_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=32),
            preserve_default=False,
        ),
    ]