# Generated by Django 4.2.7 on 2023-12-07 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_song_audio_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusermodel',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='User_images/'),
        ),
    ]
