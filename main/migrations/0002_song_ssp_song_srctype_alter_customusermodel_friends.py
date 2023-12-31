# Generated by Django 4.2.7 on 2023-11-23 11:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='SSP',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='srctype',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customusermodel',
            name='friends',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
