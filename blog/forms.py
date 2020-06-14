from django import forms
from . import models

from pagedown.widgets import PagedownWidget


class CreateArticle(forms.ModelForm):
    body = forms.CharField(widget=PagedownWidget)
    date_published = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = models.Article
        fields = ['title', 'description', 'body',
                  'image', 'draft', 'date_published',
                  'lick_string', 'transpose_string']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['description'].widget.attrs['id'] = 'textfield_description'
    #     self.fields['body'].widget.attrs['id'] = 'textfield_body'
