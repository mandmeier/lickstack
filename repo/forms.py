from django import forms
from .models import Lick


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


"""

class LickForm(forms.ModelForm):

    class Meta:
        model = Lick
        fields = ('file', 'key1_1', 'key1_2', 'key1_3', 'key1_4', 'genre',)


class LickForm(forms.ModelForm):

    class Meta:
        model = Lick
        fields = ('file', 'instrument', 'key1_1',
                  'key1_2', 'key1_3', 'key1_4', 'genre',)
        widgets = {
            'genre': forms.TextInput(attrs={'class': 'form-control'})
        }



    # Add some custom validation to check audio files
     def clean_audio_file(self):
         file = self.cleaned_data.get('file',False):
         if file:
             if file.size > 1*1024*1024:
                   raise ValidationError("Audio file too large ( > 1mb )")
             if not file.content-type in ["audio/mpeg","audio/wav"]:
                   raise ValidationError("please submit mpeg")
             if not os.path.splitext(file.name)[1] in [".mp3",".wav" ...]:
                   raise ValidationError("Doesn't have proper extension")
             # Here we need to now to read the file and see if it's actually
             # a valid audio file. I don't know what the best library is to
             # to do this
             if not some_lib.is_audio(file.content):
                   raise ValidationError("Not a valid audio file")
             return file
         else:
             raise ValidationError("Couldn't read uploaded file")
"""
