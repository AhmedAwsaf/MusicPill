from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .decorator import user_type_required
from django.db.models import Count,Q
from main.models import *
from django.views.generic import ListView
from forms.forms import *
import random

# Create your views here.
def home_view(request):
    quotes = ['Gucci gang, Gucci gang, Gucci gang, Gucci gang (Gucci gang) - Lil Pump','WE THE BEST MUSIC - DJ KHALID',"It's my life It's now or never - Bon Jovi","Hat down, cross-town, livin' like a rockstar Spent a lot of money on my brand-new guitar - Lil Nas X"]
    quote = random.choice(quotes)
    return render(request, 'home.html',{'quote': quote})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def player_view(request):
    songs = Song.objects.all()
    
    c_songs = Song.objects.filter(artist__user_type='artist')
    random_songs = list(c_songs)
    random.shuffle(random_songs)
    
    featured = random_songs[:4]
    playlists = Playlist.objects.filter(owner=request.user).annotate(song_count=Count('songs'))
    lyrics = Lyric.objects.all()
    friends = request.user.friends.all()
    oplaylists = Playlist.objects.filter(owner__in=request.user.friends.all()).annotate(song_count=Count('songs'))
    albums = Album.objects.filter(artist__in=request.user.friends.all())
    myalbums = Album.objects.filter(artist=request.user)
    
    return render(request, 'player.html',{'songs':songs,'playlists':playlists,'lyrics':lyrics,'friends':friends,'featured':featured,'oplaylists':oplaylists,'albums':albums,'myalbums':myalbums})

@login_required
def playlist_detail(request, playlist_id):
    playlists = Playlist.objects.filter(owner=request.user).annotate(song_count=Count('songs'))
    playlist = get_object_or_404(Playlist, id=playlist_id)
    
    return render(request, 'playlist_detail.html', {'playlist': playlist,'playlists':playlists})

@login_required
def userprofile(request,user_id):
    main_user = get_object_or_404(CustomUserModel, id=user_id)
    posts = Post.objects.filter(user=main_user)
    playlists = Playlist.objects.filter(owner=request.user).annotate(song_count=Count('songs'))
    songs = Song.objects.filter(artist=main_user)
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user 
            post.save()
            referring_url = request.META.get('HTTP_REFERER', '/')
    
            return redirect(referring_url)
        else:
            return render(request,'User_profile.html',{'main_user':main_user,'playlists':playlists,'songs':songs,'post_form':post_form,'posts':posts})
    if main_user.user_type=="artist" and request.user == main_user:
        post_form = PostForm()
    else:
        post_form = None
    
    
    return render(request,'User_profile.html',{'main_user':main_user,'playlists':playlists,'songs':songs,'post_form':post_form,'posts':posts})

@login_required
def delete_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    if request.user == post.user:
        post.delete()

    referring_url = request.META.get('HTTP_REFERER', '/')
    
    return redirect(referring_url)



@login_required
def add_friend_view(request, friend_id):
    friend = get_object_or_404(CustomUserModel, id=friend_id)
    current_user = request.user
    current_user.add_friend(friend)
    
    return redirect('user_list')

@login_required
def remove_friend_view(request, friend_id):
    friend = get_object_or_404(CustomUserModel, id=friend_id)

    current_user = request.user
    current_user.remove_friend(friend)

    return redirect('user_list')

class UserListView(ListView):
    model = CustomUserModel
    template_name = 'user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        queryset = CustomUserModel.objects.all()
        search_query = self.request.GET.get('search_query')

        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(bio__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = UserSearchForm(self.request.GET)
        return context
    
@login_required
def add_song_playlist_view(request, playlist_id, song_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    song_id = get_object_or_404(Song, id=song_id)
    
    if playlist.owner == request.user:
        playlist.add_song(song_id)
    
    referring_url = request.META.get('HTTP_REFERER', '/')
    
    return redirect(referring_url)
    

@login_required
def remove_song_playlist_view(request, playlist_id, song_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    song_id = get_object_or_404(Song, id=song_id)
    
    if playlist.owner == request.user:
        playlist.remove_song(song_id)
        
    referring_url = request.META.get('HTTP_REFERER', '/')
    
    return redirect(referring_url)

@login_required
def add_song_album_view(request, album_id, song_id):
    album = get_object_or_404(Album, id=album_id)
    albumsongs = get_object_or_404(AlbumSongs, album=album)
    song = get_object_or_404(Song, id=song_id)
    
    if album.artist == request.user and song.artist == request.user:
        albumsongs.add_song(song)
        song.add_album(album)
    
    referring_url = request.META.get('HTTP_REFERER', '/')
    
    return redirect(referring_url)
    

@login_required
def remove_song_album_view(request, album_id, song_id):
    album = get_object_or_404(Album, id=album_id)
    albumsongs = get_object_or_404(AlbumSongs, album=album)
    song = get_object_or_404(Song, id=song_id)
    
    if album.artist == request.user and song.artist == request.user:
        albumsongs.remove_song(song)
        song.remove_album()
    
    referring_url = request.META.get('HTTP_REFERER', '/')
    
    return redirect(referring_url)

@login_required
def album_detail(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    albumsongs = AlbumSongs.objects.get(album=album)
    
    friendalbums = Album.objects.filter(artist__in=request.user.friends.all())
    myalbums = Album.objects.filter(artist=request.user)
    
    
    return render(request, 'album_detail.html', {'album': album,'albumsongs':albumsongs,'friendalbums':friendalbums,'myalbums':myalbums})

@login_required
@user_type_required(['staff','admin'])
def staff_dashboard(request):

    users = CustomUserModel.objects.exclude(id=request.user.id).exclude(user_type='admin')
    emotions = Emotion.objects.all()
    genre = Genre.objects.all()
    
    return render(request,"Staff_Dashboard.html",{'users':users,'emotions':emotions,'genres':genre})

@login_required
@user_type_required(['staff','admin'])
def active(request, u_id):
    user = get_object_or_404(CustomUserModel, id=u_id)
    if user.is_active == False:
        user.is_active = True
    else:
        user.is_active = False
    user.save()

    return redirect('staff_dashboard')

@login_required
@user_type_required(['staff','admin'])
def c_certified(request, u_id):
    user = get_object_or_404(CustomUserModel, id=u_id)

    user.user_type = 'artist'
    user.save()

    return redirect('staff_dashboard')
@login_required
@user_type_required(['staff','admin'])
def c_staff(request, u_id):
    user = get_object_or_404(CustomUserModel, id=u_id)

    user.user_type = 'staff'
    user.save()

    return redirect('staff_dashboard')
@login_required
@user_type_required(['staff','admin'])
def c_standard(request, u_id):
    user = get_object_or_404(CustomUserModel, id=u_id)

    user.user_type = 'standard'
    user.save()

    return redirect('staff_dashboard')
