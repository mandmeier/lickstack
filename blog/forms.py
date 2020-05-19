from django import forms
from . import models


class CreateArticle(forms.ModelForm):
    class Meta:
        model = models.Article
        fields = ['title', 'description', 'body', 'image']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['description'].widget.attrs['id'] = 'textfield_description'
    #     self.fields['body'].widget.attrs['id'] = 'textfield_body'
