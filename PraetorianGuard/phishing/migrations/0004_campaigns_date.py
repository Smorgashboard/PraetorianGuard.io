# Generated by Django 4.1.3 on 2022-11-21 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phishing', '0003_rename_campaings_campaigns_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaigns',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
