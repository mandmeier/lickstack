from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


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
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    counter = models.IntegerField(default=1)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    favorite = models.ManyToManyField(
        User, related_name='favorite', blank=True)
    tags = TaggableManager()

    TS_CHOICES = [('44', '4/4'), ('34', '3/4')]

    time_signature = models.CharField(
        max_length=5, choices=TS_CHOICES, default='4/4')

    KEY_CHOICES = [
        ('.', '-'),
        (('C'), (
            ('_C_', 'C'),
            ('_C_m', 'Cm'),
            ('_C_7', 'C7'),
            ('_C_m7', 'Cm7'),
            ('_C_maj7', 'CΔ'),
            ('_C_6', 'C6'),
            ('_C_m7b5', 'Cm7b5'),
            ('_C_dim', 'Co'),
        )),
        (('B'), (
            ('_B_', 'B'),
            ('_B_m', 'Bm'),
            ('_B_7', 'B7'),
            ('_B_m7', 'Bm7'),
            ('_B_maj7', 'BΔ'),
            ('_B_6', 'B6'),
            ('_B_m7b5', 'Bm7b5'),
            ('_B_dim', 'Bo'),
        )),
        (('Bb'), (
            ('_Bb_', 'Bb'),
            ('_Bb_m', 'Bbm'),
            ('_Bb_7', 'Bb7'),
            ('_Bb_m7', 'Bbm7'),
            ('_Bb_maj7', 'BbΔ'),
            ('_Bb_6', 'Bb6'),
            ('_Bb_m7b5', 'Bbm7b5'),
            ('_Bb_dim', 'Bbo'),
        )),
        (('A'), (
            ('_A_', 'A'),
            ('_A_m', 'Am'),
            ('_A_7', 'A7'),
            ('_A_m7', 'Am7'),
            ('_A_maj7', 'AΔ'),
            ('_A_6', 'A6'),
            ('_A_m7b5', 'Am7b5'),
            ('_A_dim', 'Ao'),
        )),
        (('Ab'), (
            ('_Ab_', 'Ab'),
            ('_Ab_m', 'Abm'),
            ('_Ab_7', 'Ab7'),
            ('_Ab_m7', 'Abm7'),
            ('_Ab_maj7', 'AbΔ'),
            ('_Ab_6', 'Ab6'),
            ('_Ab_m7b5', 'Abm7b5'),
            ('_Ab_dim', 'Abo'),
        )),
        (('G'), (
            ('_G_', 'G'),
            ('_G_m', 'Gm'),
            ('_G_7', 'G7'),
            ('_G_m7', 'Gm7'),
            ('_G_maj7', 'GΔ'),
            ('_G_6', 'G6'),
            ('_G_m7b5', 'Gm7b5'),
            ('_G_dim', 'Go'),
        )),
        (('Gb'), (
            ('_Gb_', 'Gb'),
            ('_Gb_m', 'Gbm'),
            ('_Gb_7', 'Gb7'),
            ('_Gb_m7', 'Gbm7'),
            ('_Gb_maj7', 'GbΔ'),
            ('_Gb_6', 'Gb6'),
            ('_Gb_m7b5', 'Gbm7b5'),
            ('_Gb_dim', 'Gbo'),
        )),
        (('F'), (
            ('_F_', 'F'),
            ('_F_m', 'Fm'),
            ('_F_7', 'F7'),
            ('_F_m7', 'Fm7'),
            ('_F_maj7', 'FΔ'),
            ('_F_6', 'F6'),
            ('_F_m7b5', 'Fm7b5'),
            ('_F_dim', 'Fo'),
        )),
        (('E'), (
            ('_E_', 'E'),
            ('_E_m', 'Em'),
            ('_E_7', 'E7'),
            ('_E_m7', 'Em7'),
            ('_E_maj7', 'EΔ'),
            ('_E_6', 'E6'),
            ('_E_m7b5', 'Em7b5'),
            ('_E_dim', 'Eo'),
        )),
        (('Eb'), (
            ('_Eb_', 'Eb'),
            ('_Eb_m', 'Ebm'),
            ('_Eb_7', 'Eb7'),
            ('_Eb_m7', 'Ebm7'),
            ('_Eb_maj7', 'EbΔ'),
            ('_Eb_6', 'Eb6'),
            ('_Eb_m7b5', 'Ebm7b5'),
            ('_Eb_dim', 'Ebo'),
        )),
        (('D'), (
            ('_D_', 'D'),
            ('_D_m', 'Dm'),
            ('_D_7', 'D7'),
            ('_D_m7', 'Dm7'),
            ('_D_maj7', 'DΔ'),
            ('_D_6', 'D6'),
            ('_D_m7b5', 'Dm7b5'),
            ('_D_dim', 'Do'),
        )),
        (('Db'), (
            ('_Db_', 'Db'),
            ('_Db_m', 'Dbm'),
            ('_Db_7', 'Db7'),
            ('_Db_m7', 'Dbm7'),
            ('_Db_maj7', 'DbΔ'),
            ('_Db_6', 'Db6'),
            ('_Db_m7b5', 'Dbm7b5'),
            ('_Db_dim', 'Dbo'),
        )),
    ]
    m1_b1 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    m1_b2 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    m1_b3 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    m1_b4 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    m2_b1 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    m2_b2 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    m2_b3 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    m2_b4 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    m3_b1 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    m3_b2 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    m3_b3 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    m3_b4 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    m4_b1 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    m4_b2 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    m4_b3 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    m4_b4 = models.CharField(
        max_length=10,
        choices=KEY_CHOICES,
        default='-',
    )
    chord_seq = models.CharField(
        max_length=100, default='x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x')

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


"""
    def save(self, *args, **kwargs):
        self.chord_seq = (
            "x" + self.m1_b1 +
            "x" + self.m1_b2 +
            "x" + self.m1_b3 +
            "x" + self.m1_b4 +
            "x" + self.m2_b1 +
            "x" + self.m2_b2 +
            "x" + self.m2_b3 +
            "x" + self.m2_b4 +
            "x" + self.m3_b1 +
            "x" + self.m3_b2 +
            "x" + self.m3_b3 +
            "x" + self.m3_b4 +
            "x" + self.m4_b1 +
            "x" + self.m4_b2 +
            "x" + self.m4_b3 +
            "x" + self.m4_b4 + "x"
        )
        super().save(*args, **kwargs)
"""
