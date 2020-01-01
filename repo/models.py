from django.db import models
from django.utils import timezone


class Genre(models.Model):
    name = models.CharField(
        max_length=200, help_text='Enter a genre (e.g. Jazz, Blues)')

    def __str__(self):
        return self.name


class Lick(models.Model):
    # file will be uploaded to MEDIA_ROOT/lick_uploads
    file = models.FileField(upload_to='lick_uploads/')
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        name = str(self.genre) + "_" + "username" + "_" + str(self.date_posted)
        return name
