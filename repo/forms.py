from django import forms
from .models import Lick


class LickForm(forms.ModelForm):

    class Meta:
        model = Lick
        fields = ('file', 'genre',)


"""
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
