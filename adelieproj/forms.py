from django.forms import ModelForm
from adelieproj.models import Picture

class PictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = ['picture', 'caption']
