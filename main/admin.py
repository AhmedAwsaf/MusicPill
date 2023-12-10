from django.contrib import admin
from .models import *

# Register your models here.
class CustomUserModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'bio', 'image', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'bio')

admin.site.register(CustomUserModel, CustomUserModelAdmin)

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Genre, GenreAdmin)

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date')
    search_fields = ('title', 'artist__username')

admin.site.register(Album, AlbumAdmin)

class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date', 'duration', 'podcast')
    list_filter = ('podcast', 'release_date')
    search_fields = ('title', 'artist__username')

admin.site.register(Song, SongAdmin)

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner')
    search_fields = ('title', 'owner__username')

admin.site.register(Playlist, PlaylistAdmin)

class InvitesAdmin(admin.ModelAdmin):
    list_display = ('user', 'label', 'approved')
    list_filter = ('approved',)
    search_fields = ('user__username', 'label')

admin.site.register(Invites, InvitesAdmin)

class LyricAdmin(admin.ModelAdmin):
    list_display = ('song', 'text')
    search_fields = ('song__title',)

admin.site.register(Lyric, LyricAdmin)

class AlbumSongsAdmin(admin.ModelAdmin):
    list_display = ('album',)
    search_fields = ('album__title',)

admin.site.register(AlbumSongs, AlbumSongsAdmin)

class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

admin.site.register(Preference, PreferenceAdmin)

admin.site.register(Post)
admin.site.register(CertifiedUser)
admin.site.register(Emotion)