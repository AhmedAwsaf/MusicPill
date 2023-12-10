from django.urls import path
from player.views import *
from django.conf import settings
from django.conf.urls.static import static
from forms.views import *
from player.views import *


urlpatterns = [
    path('',home_view,name='home'),
    path('web.app/',player_view,name='webplayer'),
    path('user_profile/<int:user_id>/',userprofile,name='user_profile'),
    path('login/', user_login, name='user_login'),
    path('register/', register_user, name='register_user'),
    path('logout/', logout_view, name='logout_user'),
    path('add_emotion/', add_emotion, name='add_emotion'),
    path('add_genre/', add_genre, name='add_genre'),
    
    path('add_podcast/', add_podcast, name='add_podcast'),
    path('add_song/', add_song, name='add_song'),
    path('add_lyric/', add_lyric, name='add_lyric'),
    path('delete_song/<int:u_id>/', delete_song, name='delete_song'),
    
    path('add_album/', add_album, name='add_album'),
    path('album/<int:album_id>/', album_detail, name='album_detail'),
    path('album/add/<int:album_id>/<int:song_id>/', add_song_album_view, name='add_song_album_view'),
    path('album/remove/<int:album_id>/<int:song_id>/', remove_song_album_view, name='remove_song_album_view'),
    path('remove_album/<int:album_id>/', remove_album, name='remove_album'),
    
    
    path('add_playlist/', add_playlist, name='add_playlist'),
    path('playlist/<int:playlist_id>/', playlist_detail, name='playlist_detail'),
    path('remove_playlist/<int:playlist_id>', remove_playlist, name='remove_playlist'),
    
    path('users/', UserListView.as_view(), name='user_list'),
    path('add-friend/<int:friend_id>/', add_friend_view, name='add_friend'),
    path('remove-friend/<int:friend_id>/', remove_friend_view, name='remove_friend'),
    
    path('add-song-to-playlist/<int:playlist_id>/<int:song_id>/', add_song_playlist_view, name='add_song_playlist'),
    path('remove-song-from-playlist/<int:playlist_id>/<int:song_id>/', remove_song_playlist_view, name='remove_song_playlist'),
    
    path('update_album/<int:album_id>/', update_album, name='update_album'),
    path('update_song/<int:song_id>/', update_song, name='update_song'),
    path('update_playlist/<int:playlist_id>/', update_playlist, name='update_playlist'),
    path('update_profile/<int:user_id>/', update_profile, name='update_profile'),
    path('update_genre/<int:genre_id>/', update_genre, name='update_genre'),
    path('update_emotion/<int:emotion_id>/', update_emotion, name='update_emotion'),
    
    path('register_certified_user/', certified_user_registration_view, name='register_certified_user'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    
    path('staff_dashboard/', staff_dashboard, name='staff_dashboard'),
    path('Staff_dashboard/activate_toggle/<int:u_id>/', active , name='activate_toggle'),
    path('staff_dashboard/c_staff/<int:u_id>/', c_staff, name='c_staff'),
    path('staff_dashboard/c_standard/<int:u_id>/', c_standard, name='c_standard'),
    path('staff_dashboard/c_certified/<int:u_id>/', c_certified, name='c_certified'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)