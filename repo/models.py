from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

import re


def get_transpose_rule(chord_seq):
    chords = chord_seq.split('x')[1:17]
    note_regex = r'_([a-gA-g#]+)_'
    notes = []
    indices = []
    for index, chord in enumerate(chords):
        if chord == '.':
            notes.append('.')
        else:
            chord = re.search(note_regex, chord).group(0).replace('_', '')
            notes.append(chord)
            indices.append(index)
    notes = list(filter(lambda a: a != '.', notes))
    transpose_rule = ['b' for i in range(16)]
    for index, note in enumerate(notes):
        # b to right condition
        if index != len(notes) - 1:
            b_to_right = 'b' in notes[index + 1]
        else:
            b_to_right = False

        if '#' in note:
            transpose_rule[indices[index]] = 'h'
            if index != 0:
                transpose_rule[indices[index - 1]] = 'h'

        elif note == 'B':
            # C to left condition
            if index != 0:
                c_to_left = notes[index - 1] == 'C'
            else:
                c_to_left = False
            # C to right condition
            if index != len(notes) - 1:
                c_to_right = notes[index + 1] == 'C'
            else:
                c_to_right = False
            # C sandwich cpndition
            if c_to_left and not c_to_right:
                c_sandwich = True
            else:
                c_sandwich = False
            if b_to_right or c_sandwich:
                transpose_rule[indices[index]] = 'b'
            else:
                transpose_rule[indices[index]] = 'h'
        elif note == 'E':
            # F to left condition
            if index != 0:
                f_to_left = notes[index - 1] == 'F'
            else:
                f_to_left = False
            # F to right condition
            if index != len(notes) - 1:
                f_to_right = notes[index + 1] == 'F'
            else:
                f_to_right = False
            # F sandwich cpndition
            if f_to_left and not f_to_right:
                f_sandwich = True
            else:
                f_sandwich = False
            if b_to_right or f_sandwich:
                transpose_rule[indices[index]] = 'b'
            else:
                transpose_rule[indices[index]] = 'h'
        else:
            transpose_rule[indices[index]] = 'b'
    return ','.join(transpose_rule)


def get_chord_seq_search(chord_seq):
    sharps = ['C#', 'D#', 'F#', 'G#', 'A#']
    flats = ['Db', 'Eb', 'Gb', 'Ab', 'Bb']
    for s, f in zip(sharps, flats):
        chord_seq = chord_seq.replace(s, f)
    return chord_seq


class Instrument(models.Model):
    name = models.CharField(
        max_length=200, help_text='Enter an instrument (e.g. Piano, Guitar)', default='not specified')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Lick(models.Model):
    # file will be uploaded to MEDIA_ROOT/lick_uploads
    file = models.FileField(upload_to='lick_uploads/')
    instrument = models.ForeignKey(
        Instrument, on_delete=models.PROTECT, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    counter = models.IntegerField(default=1)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    favorite = models.ManyToManyField(
        User, related_name='favorite', blank=True)
    tags = TaggableManager()

    TS_CHOICES = [('44', '4/4'), ('34', '3/4')]

    time_signature = models.CharField(
        max_length=5, choices=TS_CHOICES, default='4/4')

    chord_seq = models.CharField(
        max_length=150, default='x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x')
    chord_seq_search = models.CharField(
        max_length=150, default='x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x')
    transpose_rule = models.CharField(
        max_length=100, default='b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b')

    def __str__(self):
        tagstr = '-'.join(self.tags.names())
        name = '#' + str(self.id) + "-" + tagstr + "-" + \
            str(self.author) + "-" + str(self.date_posted)
        return name

    def get_absolute_url(self):
        return reverse('lick-detail', kwargs={'pk': self.pk})

    # delete audio file from file system when delete lick model instance
    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()

    def total_faves(self):
        return self.favorite.count()

    def save(self, *args, **kwargs):
        self.transpose_rule = get_transpose_rule(self.chord_seq)
        self.chord_seq_search = get_chord_seq_search(self.chord_seq)
        super().save(*args, **kwargs)


@receiver(models.signals.pre_delete, sender=Lick)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.file.delete(save=False)
