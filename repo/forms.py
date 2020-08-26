from django import forms
from django.db import models
from .models import Lick
from django.core.exceptions import ValidationError
import os


class LickForm(forms.ModelForm):
  TS_CHOICES = [('44', '4/4'), ('34', '3/4')]
  time_signature = forms.ChoiceField(
      choices=TS_CHOICES, initial='44', widget=forms.RadioSelect, label='')
  other = forms.CharField(required=False, label='')

  class Meta:
    model = Lick
    fields = ('file', 'instrument', 'time_signature',
              'tags', 'chord_seq', 'description')

    labels = {
        'file': '',
        'tags': '',
        'other': '',
        'chord_seq': '',
        'instrument': '',
        'description': '',
    }
    help_texts = {
        'file': '',
        'tags': '',
    }
    error_messages = {
        'tags': {
            'required': 'Please enter between 1 and 5 tags.',
        }
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['other'].widget.attrs['placeholder'] = 'Please specify'
    self.fields['file'].widget.attrs['id'] = 'inpFile'

  # validate uploaded file for extension and file size
  def clean_file(self):
    file = self.cleaned_data['file']
    valid_extensions = ['.m4a', '.mp3', '.ogg']
    ext = os.path.splitext(file.name)[1]
    if not ext.lower() in valid_extensions:
      raise ValidationError('Please upload a .mp3 or .m4a audio file.')
    elif file.size > 1 * 1024 * 1024:
      raise forms.ValidationError(
          f'File is too large ({str(round(file.size/(1024 * 1024), 2))} Mb). Please stay below 1 Mb. Consider shortening it.')
    else:
      return file
