from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Genre(models.Model):
    name = models.CharField(
        max_length=200, help_text='Enter a genre (e.g. Jazz, Blues)')

    def __str__(self):
        return self.name


class Instrument(models.Model):
    name = models.CharField(
        max_length=200, help_text='Enter an instrument (e.g. Piano, Guitar)', default='not specified')

    def __str__(self):
        return self.name


class Lick(models.Model):
    # file will be uploaded to MEDIA_ROOT/lick_uploads
    file = models.FileField(upload_to='lick_uploads/')
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, null=True)
    instrument = models.ForeignKey(
        Instrument, on_delete=models.PROTECT, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    counter = models.IntegerField(default=1)
    KEY_CHOICES = [
        ('-', '-'),
        (('C'), (
            ('C', 'C'),
            ('Cm', 'Cm'),
            ('C7', 'C7'),
            ('Cm7', 'Cm7'),
            ('CΔ', 'CΔ'),
            ('C6', 'C6'),
            ('Cø', 'Cø'),
            ('Co', 'Co'),
        )),
        (('B'), (
            ('B', 'B'),
            ('Bm', 'Bm'),
            ('B7', 'B7'),
            ('Bm7', 'Bm7'),
            ('BΔ', 'BΔ'),
            ('B6', 'B6'),
            ('Bø', 'Bø'),
            ('Bo', 'Bo'),
        )),
        (('Bb'), (
            ('Bb', 'Bb'),
            ('Bbm', 'Bbm'),
            ('Bb7', 'Bb7'),
            ('Bbm7', 'Bbm7'),
            ('BbΔ', 'BbΔ'),
            ('Bb6', 'Bb6'),
            ('Bbø', 'Bbø'),
            ('Bbo', 'Bbo'),
        )),
        (('A'), (
            ('A', 'A'),
            ('Am', 'Am'),
            ('A7', 'A7'),
            ('Am7', 'Am7'),
            ('AΔ', 'AΔ'),
            ('A6', 'A6'),
            ('Aø', 'Aø'),
            ('Ao', 'Ao'),
        )),
        (('Ab'), (
            ('Ab', 'Ab'),
            ('Abm', 'Abm'),
            ('Ab7', 'Ab7'),
            ('Abm7', 'Abm7'),
            ('AbΔ', 'AbΔ'),
            ('Ab6', 'Ab6'),
            ('Abø', 'Abø'),
            ('Abo', 'Abo'),
        )),
        (('G'), (
            ('G', 'G'),
            ('Gm', 'Gm'),
            ('G7', 'G7'),
            ('Gm7', 'Gm7'),
            ('GΔ', 'GΔ'),
            ('G6', 'G6'),
            ('Gø', 'Gø'),
            ('Go', 'Go'),
        )),
        (('Gb'), (
            ('Gb', 'Gb'),
            ('Gbm', 'Gbm'),
            ('Gb7', 'Gb7'),
            ('Gbm7', 'Gbm7'),
            ('GbΔ', 'GbΔ'),
            ('Gb6', 'Gb6'),
            ('Gbø', 'Gbø'),
            ('Gbo', 'Gbo'),
        )),
        (('F'), (
            ('F', 'F'),
            ('Fm', 'Fm'),
            ('F7', 'F7'),
            ('Fm7', 'Fm7'),
            ('FΔ', 'FΔ'),
            ('F6', 'F6'),
            ('Fø', 'Fø'),
            ('Fo', 'Fo'),
        )),
        (('E'), (
            ('E', 'E'),
            ('Em', 'Em'),
            ('E7', 'E7'),
            ('Em7', 'Em7'),
            ('EΔ', 'EΔ'),
            ('E6', 'E6'),
            ('Eø', 'Eø'),
            ('Eo', 'Eo'),
        )),
        (('Eb'), (
            ('Eb', 'Eb'),
            ('Ebm', 'Ebm'),
            ('Eb7', 'Eb7'),
            ('Ebm7', 'Ebm7'),
            ('EbΔ', 'EbΔ'),
            ('Eb6', 'Eb6'),
            ('Ebø', 'Ebø'),
            ('Ebo', 'Ebo'),
        )),
        (('D'), (
            ('D', 'D'),
            ('Dm', 'Dm'),
            ('D7', 'D7'),
            ('Dm7', 'Dm7'),
            ('DΔ', 'DΔ'),
            ('D6', 'D6'),
            ('Dø', 'Dø'),
            ('Do', 'Do'),
        )),
        (('Db'), (
            ('Db', 'Db'),
            ('Dbm', 'Dbm'),
            ('Db7', 'Db7'),
            ('Dbm7', 'Dbm7'),
            ('DbΔ', 'DbΔ'),
            ('Db6', 'Db6'),
            ('Dbø', 'Dbø'),
            ('Dbo', 'Dbo'),
        )),
    ]
    beat1 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    beat2 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    beat3 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    beat4 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    beat5 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    beat6 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    beat7 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    beat8 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    beat9 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    beat10 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    beat11 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    beat12 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    beat13 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    beat14 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    beat15 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    beat16 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )

    def __str__(self):
        name = str(self.genre) + "_" + str(self.author) + \
            "_" + str(self.date_posted)
        return name

    def get_absolute_url(self):
        return reverse('lick-detail', kwargs={'pk': self.pk})
