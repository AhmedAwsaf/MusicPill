from django.contrib.auth.models import AbstractUser,User
from django.db import models
import os
from django.utils.text import slugify
from django.contrib.auth import get_user_model as user_model


# Create your models here.
def get_song_upload_path(instance, filename):
    return os.path.join("songs", instance.artist.username, slugify(instance.title), filename)


class CustomUserModel(AbstractUser):
    USER_TYPE_CHOICES = (
        ('standard', 'Standard User'),
        ('artist', 'Artist'),
        ('admin', 'Administrator'),
        ('staff', 'Staff'),   
    )
    
    bio = models.TextField(blank=True)
    friends = models.ManyToManyField('self',blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='standard')
    image = models.ImageField(upload_to=f'User_images/', blank=True, null=True)

    def __str__(self):
        return self.username
    def add_friend(self, friend):
        if friend != self:
            self.friends.add(friend)

    def remove_friend(self, friend):
        self.friends.remove(friend)
    

class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name

class Emotion(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name

class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    release_date = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to='album_covers/', blank=True, null=True)

    def __str__(self):
        return self.title

class Song(models.Model):
    title = models.CharField(max_length=255)
    bio = models.TextField(max_length=450,blank=True,null=True)
    artist = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    SSP = models.TextField(blank=True,null=True) #SINGERSONGWRITERPRODUCER
    srctype = models.BooleanField(default=False,blank=True,null=True)
    audio_url = models.URLField(null=True,blank=True)
    audio_file = models.FileField(upload_to=get_song_upload_path,null=True,blank=True)
    cover_image = models.ImageField(upload_to='song_covers/', blank=True, null=True)
    release_date = models.DateTimeField(auto_now_add=True)
    duration = models.PositiveIntegerField(default=0)
    podcast = models.BooleanField(default=False)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True,null=True)
    nop = models.PositiveIntegerField(default=0)
    Emotion = models.ForeignKey(Emotion, on_delete=models.SET_NULL, blank=True,null=True)
    

    def __str__(self):
        return self.title
    
    def increase_play_count(self):
        self.nop += 1
        self.save()
    
    def add_album(self, album):
        self.album = album
        self.save()

    def remove_album(self):
        self.album = None
        self.save()
    
    def add_emotion(self, emotion):
        self.emotion = emotion
        self.save()

    def remove_emotion(self):
        self.emotion = None
        self.save()
    
    def add_genre(self, genre):
        self.genre = genre
        self.save()

    def remove_genre(self):
        self.genre = None
        self.save()
    

class Playlist(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song, related_name='playlists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    def add_song(self, song):
        self.songs.add(song)

    def remove_song(self, song):
        self.songs.remove(song)


class Invites(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    label = models.TextField(blank=True,null=True)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"invite {self.name}"


class Lyric(models.Model):
    song = models.OneToOneField(Song, on_delete=models.CASCADE, related_name='lyrics')
    language = models.TextField(max_length=255,default="No Language specified")
    text = models.TextField()

    def __str__(self):
        return f"Lyrics for {self.song.title}"

class AlbumSongs(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song, blank=True)
    
    def __str__(self):
        return self.album.title
    def add_song(self, song):
        self.songs.add(song)

    def remove_song(self, song):
        self.songs.remove(song)
    
class Preference(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre, related_name='prefers', blank=True)

class Restrict(models.Model):
    user = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE)
    ban = models.BooleanField(default=True)
    
#DIYA
class CertifiedUser(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    social_media_link = models.URLField(blank=True)
    location = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=155,blank=True)
    description = models.CharField(max_length=300,blank=True,null=True)
    url = models.URLField(blank=True,null=True)
    banner_image = models.ImageField(upload_to='post_banners/', blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'post of {self.title}'