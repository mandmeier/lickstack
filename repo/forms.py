from django import forms
from .models import Lick


class LickForm(forms.ModelForm):

    class Meta:
        model = Lick
        fields = ('file', 'genre',)
