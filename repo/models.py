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

    TS_CHOICES = [('4/4', '4/4'), ('3/4', '3/4')]

    time_signature = models.CharField(
        max_length=5, choices=TS_CHOICES, default='4/4')

    KEY_CHOICES = [
        ('dash', '-'),
        (('C'), (
            ('C', 'C'),
            ('Cm', 'Cm'),
            ('C7', 'C7'),
            ('Cm7', 'Cm7'),
            ('Cmaj7', 'CΔ'),
            ('C6', 'C6'),
            ('Cm7b5', 'Cø'),
            ('Cdim', 'Co'),
        )),
        (('B'), (
            ('B', 'B'),
            ('Bm', 'Bm'),
            ('B7', 'B7'),
            ('Bm7', 'Bm7'),
            ('Bmaj7', 'BΔ'),
            ('B6', 'B6'),
            ('Bm7b5', 'Bø'),
            ('Bdim', 'Bo'),
        )),
        (('Bb'), (
            ('Bb', 'Bb'),
            ('Bbm', 'Bbm'),
            ('Bb7', 'Bb7'),
            ('Bbm7', 'Bbm7'),
            ('Bbmaj7', 'BbΔ'),
            ('Bb6', 'Bb6'),
            ('Bbm7b5', 'Bbø'),
            ('Bbdim', 'Bbo'),
        )),
        (('A'), (
            ('A', 'A'),
            ('Am', 'Am'),
            ('A7', 'A7'),
            ('Am7', 'Am7'),
            ('Amaj7', 'AΔ'),
            ('A6', 'A6'),
            ('Am7b5', 'Aø'),
            ('Adim', 'Ao'),
        )),
        (('Ab'), (
            ('Ab', 'Ab'),
            ('Abm', 'Abm'),
            ('Ab7', 'Ab7'),
            ('Abm7', 'Abm7'),
            ('Abmaj7', 'AbΔ'),
            ('Ab6', 'Ab6'),
            ('Abm7b5', 'Abø'),
            ('Abdim', 'Abo'),
        )),
        (('G'), (
            ('G', 'G'),
            ('Gm', 'Gm'),
            ('G7', 'G7'),
            ('Gm7', 'Gm7'),
            ('Gmaj7', 'GΔ'),
            ('G6', 'G6'),
            ('Gm7b5', 'Gø'),
            ('Gdim', 'Go'),
        )),
        (('Gb'), (
            ('Gb', 'Gb'),
            ('Gbm', 'Gbm'),
            ('Gb7', 'Gb7'),
            ('Gbm7', 'Gbm7'),
            ('Gbmaj7', 'GbΔ'),
            ('Gb6', 'Gb6'),
            ('Gbm7b5', 'Gbø'),
            ('Gbdim', 'Gbo'),
        )),
        (('F'), (
            ('F', 'F'),
            ('Fm', 'Fm'),
            ('F7', 'F7'),
            ('Fm7', 'Fm7'),
            ('Fmaj7', 'FΔ'),
            ('F6', 'F6'),
            ('Fm7b5', 'Fø'),
            ('Fdim', 'Fo'),
        )),
        (('E'), (
            ('E', 'E'),
            ('Em', 'Em'),
            ('E7', 'E7'),
            ('Em7', 'Em7'),
            ('Emaj7', 'EΔ'),
            ('E6', 'E6'),
            ('Em7b5', 'Eø'),
            ('Edim', 'Eo'),
        )),
        (('Eb'), (
            ('Eb', 'Eb'),
            ('Ebm', 'Ebm'),
            ('Eb7', 'Eb7'),
            ('Ebm7', 'Ebm7'),
            ('Ebmaj7', 'EbΔ'),
            ('Eb6', 'Eb6'),
            ('Ebm7b5', 'Ebø'),
            ('Ebdim', 'Ebo'),
        )),
        (('D'), (
            ('D', 'D'),
            ('Dm', 'Dm'),
            ('D7', 'D7'),
            ('Dm7', 'Dm7'),
            ('Dmaj7', 'DΔ'),
            ('D6', 'D6'),
            ('Dm7b5', 'Dø'),
            ('Ddim', 'Do'),
        )),
        (('Db'), (
            ('Db', 'Db'),
            ('Dbm', 'Dbm'),
            ('Db7', 'Db7'),
            ('Dbm7', 'Dbm7'),
            ('Dbmaj7', 'DbΔ'),
            ('Db6', 'Db6'),
            ('Dbm7b5', 'Dbø'),
            ('Dbdim', 'Dbo'),
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
