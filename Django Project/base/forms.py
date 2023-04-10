from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User


class UsersCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        # exclude host and participants selection from user
        exclude = ['host', 'participants']


# The user can update the followings:
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
