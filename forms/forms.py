from django import forms
from django.contrib.auth.forms import AuthenticationForm
from main.models import *

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'cover_image']

class SongForm(forms.ModelForm):
    # srctype = forms.BooleanField(label='Default to Youtube link?', required=False)
    
    class Meta:
        model = Song
        fields = ['title', 'bio','SSP','audio_file','audio_url', 'cover_image', 'album', 'genre','Emotion']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['audio_file'].widget.attrs['accept'] = 'audio/*'
    
    def save(self, commit=True):
        song = super().save(commit=False)
        
        if commit:
            song.save()
        return song
    
class PodcastForm(forms.ModelForm):
    # srctype = forms.BooleanField(label='Default to Youtube link?', required=False)

    class Meta:
        model = Song
        fields = ['title', 'bio', 'audio_file', 'audio_url', 'cover_image', 'Emotion']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['audio_file'].widget.attrs['accept'] = 'audio/*'
    
    def save(self, commit=True):
        song = super().save(commit=False)
        if commit:
            song.save()
        return song

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

class EmotionForm(forms.ModelForm):
    class Meta:
        model = Emotion
        fields = ['name']
        
class PlaylistCreateForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['title']
        
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))   

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUserModel
        fields = ['username', 'email', 'bio', 'image']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class LyricForm(forms.ModelForm):
    class Meta:
        model = Lyric
        fields = ['song', 'language', 'text']

    def __init__(self, user, *args, **kwargs):
        super(LyricForm, self).__init__(*args, **kwargs)
        self.fields['song'].queryset = Song.objects.filter(artist=user)

class UserSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False, label='Search Users')
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUserModel
        fields = ['username', 'bio', 'image']  

     
#DIYA
class CertifiedUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CertifiedUser
        fields = [ 'date_of_birth', 'social_media_link', 'location']
    
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'url', 'banner_image']
        
#YASIN

class ChangeRoleForm(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUserModel.objects.all())
    new_role = forms.ChoiceField(
        choices=[('standard', 'Standard User'), ('certified', 'Certified User')]
    )
class UserActivationForm(forms.Form):
    user_ids = forms.ModelMultipleChoiceField(
    queryset=CustomUserModel.objects.all(),
    widget=forms.CheckboxSelectMultiple
    )
    is_active = forms.BooleanField(initial=True, required=False)