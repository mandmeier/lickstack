from django import forms
from .models import Lick
from django.core.exceptions import ValidationError
import os


class LickForm(forms.ModelForm):

  class Meta:
    model = Lick
    fields = ('file', 'instrument', 'genre', 'time_signature',
              'm1_b1', 'm1_b2', 'm1_b3', 'm1_b4',
              'm2_b1', 'm2_b2', 'm2_b3', 'm2_b4',
              'm3_b1', 'm3_b2', 'm3_b3', 'm3_b4',
              'm4_b1', 'm4_b2', 'm4_b3', 'm4_b4',
              )

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['file'].widget.attrs['id'] = 'inpFile'
    self.fields['m1_b4'].widget.attrs['class'] = 'ts44'
    self.fields['m2_b4'].widget.attrs['class'] = 'ts44'
    self.fields['m3_b4'].widget.attrs['class'] = 'ts44'
    self.fields['m4_b4'].widget.attrs['class'] = 'ts44'

  # validate uploaded file for extension and file size
  def clean_file(self):
    file = self.cleaned_data['file']
    valid_extensions = ['.m4a', '.mp3']
    ext = os.path.splitext(file.name)[1]
    if not ext.lower() in valid_extensions:
      raise ValidationError('Please upload a .mp3 or .m4a audio file.')
    elif file.size > 1 * 1024 * 1024:
      raise forms.ValidationError(
          f'File is too large ({str(round(file.size/(1024 * 1024), 2))} Mb). Please stay below 1 Mb. Consider shortening it.')
    else:
      return file
