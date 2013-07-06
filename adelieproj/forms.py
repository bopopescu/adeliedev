from django.forms import ModelForm
from adelieproj.models import GamePicture

class GamePictureForm(ModelForm):
    class Meta:
        model = GamePicture
        fields = ['picture', 'caption']