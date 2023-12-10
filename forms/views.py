from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import authenticate, login
from .forms import *

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate the user
            user = form.get_user()
            login(request, user)
            return redirect('webplayer')  
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user_login')  
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def add_emotion(request):
    if request.method == 'POST':
        form = EmotionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('webplayer')  
    else:
        form = EmotionForm()

    return render(request, 'add_Emotion.html', {'form': form})

@login_required
def add_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('webplayer')  
    else:
        form = GenreForm()

    return render(request, 'add_genre.html', {'form': form})


@login_required
def add_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save(commit=False)
            album.artist = request.user
            album.save()
            
            new_object = AlbumSongs(album=album)
            new_object.save()
            return redirect('webplayer')  
    else:
        form = AlbumForm()

    return render(request, 'add_album.html', {'form': form})

@login_required
def remove_album(request,album_id):
    album = get_object_or_404(Album, id=album_id)
    albumSongs = get_object_or_404(AlbumSongs, album=album)
    if request.user == album.artist:
        album.delete()
        albumSongs.delete()

    return redirect('webplayer')

@login_required
def add_song(request):
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.artist = request.user
            song.save()
            return redirect('webplayer')  
    else:
        form = SongForm()

    return render(request, 'add_song.html', {'form': form})

def delete_song(request,u_id):
    song = get_object_or_404(Song, id=u_id)
    if request.user == song.artist:
        song.delete()
    
    return redirect('webplayer')  

@login_required
def add_podcast(request):
    if request.method == 'POST':
        form = PodcastForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save(commit=False)
            song.artist = request.user
            song.podcast = True
            song.save()
            return redirect('webplayer')  
    else:
        form = PodcastForm()

    return render(request, 'add_podcast.html', {'form': form})

@login_required
def add_playlist(request):
    if request.method == 'POST':
        form = PlaylistCreateForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.owner = request.user
            playlist.save()
            return redirect('webplayer')  
    else:
        form = PlaylistCreateForm()

    return render(request, 'add_playlist.html', {'form': form})

@login_required
def remove_playlist(request,playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    if request.user == playlist.owner:
        playlist.delete()

    return redirect('webplayer')

@login_required
def add_lyric(request):
    if request.method == 'POST':
        form = LyricForm(request.user, request.POST)
        if form.is_valid():
            lyric = form.save(commit=False)
            lyric.save()
            return redirect('webplayer')
    else:
        form = LyricForm(request.user)

    return render(request, 'add_lyrics.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def admin_add_view(request):
    return render(request, 'admindashboard.html')


@login_required
def update_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            return redirect('webplayer')
    else:
        form = AlbumForm(instance=album)

    return render(request, 'update_album.html', {'form': form})

@login_required
def update_song(request, song_id):
    song = Song.objects.get(pk=song_id)
    if request.method == 'POST':
        form = SongForm(request.POST, request.FILES, instance=song)
        if form.is_valid():
            form.save()
            return redirect('webplayer')
    else:
        form = SongForm(instance=song)

    return render(request, 'update_song.html', {'form': form})

@login_required
def update_playlist(request, playlist_id):
    playlist = Playlist.objects.get(pk=playlist_id)
    if request.method == 'POST':
        form = PlaylistCreateForm(request.POST, instance=playlist)
        if form.is_valid():
            form.save()
            return redirect('webplayer')
    else:
        form = PlaylistCreateForm(instance=playlist)
    
    return render(request, 'update_playlist.html', {'form': form})

@login_required
def update_profile(request, user_id):
    user = CustomUserModel.objects.get(pk=user_id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('webplayer')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'update_profile.html', {'form': form})

@login_required
def update_genre(request, genre_id):
    genre = CustomUserModel.objects.get(pk=genre_id)
    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            return redirect('webplayer')
    else:
        form = GenreForm(instance=genre)

    return render(request, 'update_genre.html', {'form': form})

@login_required
def update_emotion(request, emotion_id):
    emotion = CustomUserModel.objects.get(pk=emotion_id)
    if request.method == 'POST':
        form = EmotionForm(request.POST, instance=emotion)
        if form.is_valid():
            form.save()
            return redirect('webplayer')
    else:
        form = EmotionForm(instance=emotion)

    return render(request, 'update_emotion.html', {'form': form})
@login_required
def certified_user_registration_view(request):
    user = request.user
    
    if request.method == 'POST':
        form = CertifiedUserRegistrationForm(request.POST)
        if form.is_valid():
            certified_user = form.save(commit=False)
            certified_user.user = request.user 
            certified_user.save()
            
            user.user_type = 'artist'
            user.save()
            return redirect('webplayer')  # Replace 'success_page' with the actual success page URL
    else:
        form = CertifiedUserRegistrationForm()

    return render(request, 'certified_registration.html', {'form': form})

#Yasin

@login_required
def activate_deactivate_user(request):
    current_staff_user = request.user
    users = CustomUserModel.objects.exclude(user_type='staff')

    if request.method == 'POST':
        form = UserActivationForm(request.POST)
        if form.is_valid():
            user_ids = form.cleaned_data['user_ids']
            is_active = form.cleaned_data['is_active']

            # Update all selected users
            CustomUserModel.objects.filter(id__in=user_ids).update(is_active=is_active)

    else:
        form = UserActivationForm()
    return render(request, 'Staff_dashboard.html', {'form': form, 'users': users})
