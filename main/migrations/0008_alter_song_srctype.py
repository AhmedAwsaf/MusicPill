# Generated by Django 4.2.7 on 2023-12-04 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_song_srctype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='srctype',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
