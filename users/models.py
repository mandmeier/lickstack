from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from repo.models import Lick


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    liked_licks = models.ManyToManyField(
        Lick, related_name='liked_licks', blank=True)
    faved_licks = models.ManyToManyField(
        Lick, related_name='faved_licks', blank=True)
    # instrument?
    # current city?
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    TS_CHOICES = [('0', 'concert'), ('-3', 'Eb'), ('2', 'Bb')]

    instr_transpose_shift = models.CharField(
        max_length=10, choices=TS_CHOICES, default='concert')

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):  # override save method to resize profile pic if too large
    #     super().save(*args, **kwargs)  # save method of class above

    #     img = Image.open(self.image.path)

    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)

    # delete profile pic from file system when delete user
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
