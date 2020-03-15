# Generated by Django 3.0.2 on 2020-03-14 22:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a genre (e.g. Jazz, Blues)', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='not specified', help_text='Enter an instrument (e.g. Piano, Guitar)', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter a keyword', max_length=200)),
                ('genres', models.ManyToManyField(blank=True, related_name='genres', to='repo.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Lick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='lick_uploads/')),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('counter', models.IntegerField(default=1)),
                ('time_signature', models.CharField(choices=[('44', '4/4'), ('34', '3/4')], default='4/4', max_length=5)),
                ('m1_b1', models.CharField(choices=[('.', '-'), ('C', (('_C_', 'C'), ('_C_m', 'Cm'), ('_C_7', 'C7'), ('_C_m7', 'Cm7'), ('_C_maj7', 'CΔ'), ('_C_6', 'C6'), ('_C_m7b5', 'Cm7b5'), ('_C_dim', 'Co'))), ('B', (('_B_', 'B'), ('_B_m', 'Bm'), ('_B_7', 'B7'), ('_B_m7', 'Bm7'), ('_B_maj7', 'BΔ'), ('_B_6', 'B6'), ('_B_m7b5', 'Bm7b5'), ('_B_dim', 'Bo'))), ('Bb', (('_Bb_', 'Bb'), ('_Bb_m', 'Bbm'), ('_Bb_7', 'Bb7'), ('_Bb_m7', 'Bbm7'), ('_Bb_maj7', 'BbΔ'), ('_Bb_6', 'Bb6'), ('_Bb_m7b5', 'Bbm7b5'), ('_Bb_dim', 'Bbo'))), ('A', (('_A_', 'A'), ('_A_m', 'Am'), ('_A_7', 'A7'), ('_A_m7', 'Am7'), ('_A_maj7', 'AΔ'), ('_A_6', 'A6'), ('_A_m7b5', 'Am7b5'), ('_A_dim', 'Ao'))), ('Ab', (('_Ab_', 'Ab'), ('_Ab_m', 'Abm'), ('_Ab_7', 'Ab7'), ('_Ab_m7', 'Abm7'), ('_Ab_maj7', 'AbΔ'), ('_Ab_6', 'Ab6'), ('_Ab_m7b5', 'Abm7b5'), ('_Ab_dim', 'Abo'))), ('G', (('_G_', 'G'), ('_G_m', 'Gm'), ('_G_7', 'G7'), ('_G_m7', 'Gm7'), ('_G_maj7', 'GΔ'), ('_G_6', 'G6'), ('_G_m7b5', 'Gm7b5'), ('_G_dim', 'Go'))), ('Gb', (('_Gb_', 'Gb'), ('_Gb_m', 'Gbm'), ('_Gb_7', 'Gb7'), ('_Gb_m7', 'Gbm7'), ('_Gb_maj7', 'GbΔ'), ('_Gb_6', 'Gb6'), ('_Gb_m7b5', 'Gbm7b5'), ('_Gb_dim', 'Gbo'))), ('F', (('_F_', 'F'), ('_F_m', 'Fm'), ('_F_7', 'F7'), ('_F_m7', 'Fm7'), ('_F_maj7', 'FΔ'), ('_F_6', 'F6'), ('_F_m7b5', 'Fm7b5'), ('_F_dim', 'Fo'))), ('E', (('_E_', 'E'), ('_E_m', 'Em'), ('_E_7', 'E7'), ('_E_m7', 'Em7'), ('_E_maj7', 'EΔ'), ('_E_6', 'E6'), ('_E_m7b5', 'Em7b5'), ('_E_dim', 'Eo'))), ('Eb', (('_Eb_', 'Eb'), ('_Eb_m', 'Ebm'), ('_Eb_7', 'Eb7'), ('_Eb_m7', 'Ebm7'), ('_Eb_maj7', 'EbΔ'), ('_Eb_6', 'Eb6'), ('_Eb_m7b5', 'Ebm7b5'), ('_Eb_dim', 'Ebo'))), ('D', (('_D_', 'D'), ('_D_m', 'Dm'), ('_D_7', 'D7'), ('_D_m7', 'Dm7'), ('_D_maj7', 'DΔ'), ('_D_6', 'D6'), ('_D_m7b5', 'Dm7b5'), ('_D_dim', 'Do'))), ('Db', (('_Db_', 'Db'), ('_Db_m', 'Dbm'), ('_Db_7', 'Db7'), ('_Db_m7', 'Dbm7'), ('_Db_maj7', 'DbΔ'), ('_Db_6', 'Db6'), ('_Db_m7b5', 'Dbm7b5'), ('_Db_dim', 'Dbo')))], default='-', max_length=10)),
                ('m1_b2', models.CharField(choices=[('.', '-'), ('C', (('_C_', 'C'), ('_C_m', 'Cm'), ('_C_7', 'C7'), ('_C_m7', 'Cm7'), ('_C_maj7', 'CΔ'), ('_C_6', 'C6'), ('_C_m7b5', 'Cm7b5'), ('_C_dim', 'Co'))), ('B', (('_B_', 'B'), ('_B_m', 'Bm'), ('_B_7', 'B7'), ('_B_m7', 'Bm7'), ('_B_maj7', 'BΔ'), ('_B_6', 'B6'), ('_B_m7b5', 'Bm7b5'), ('_B_dim', 'Bo'))), ('Bb', (('_Bb_', 'Bb'), ('_Bb_m', 'Bbm'), ('_Bb_7', 'Bb7'), ('_Bb_m7', 'Bbm7'), ('_Bb_maj7', 'BbΔ'), ('_Bb_6', 'Bb6'), ('_Bb_m7b5', 'Bbm7b5'), ('_Bb_dim', 'Bbo'))), ('A', (('_A_', 'A'), ('_A_m', 'Am'), ('_A_7', 'A7'), ('_A_m7', 'Am7'), ('_A_maj7', 'AΔ'), ('_A_6', 'A6'), ('_A_m7b5', 'Am7b5'), ('_A_dim', 'Ao'))), ('Ab', (('_Ab_', 'Ab'), ('_Ab_m', 'Abm'), ('_Ab_7', 'Ab7'), ('_Ab_m7', 'Abm7'), ('_Ab_maj7', 'AbΔ'), ('_Ab_6', 'Ab6'), ('_Ab_m7b5', 'Abm7b5'), ('_Ab_dim', 'Abo'))), ('G', (('_G_', 'G'), ('_G_m', 'Gm'), ('_G_7', 'G7'), ('_G_m7', 'Gm7'), ('_G_maj7', 'GΔ'), ('_G_6', 'G6'), ('_G_m7b5', 'Gm7b5'), ('_G_dim', 'Go'))), ('Gb', (('_Gb_', 'Gb'), ('_Gb_m', 'Gbm'), ('_Gb_7', 'Gb7'), ('_Gb_m7', 'Gbm7'), ('_Gb_maj7', 'GbΔ'), ('_Gb_6', 'Gb6'), ('_Gb_m7b5', 'Gbm7b5'), ('_Gb_dim', 'Gbo'))), ('F', (('_F_', 'F'), ('_F_m', 'Fm'), ('_F_7', 'F7'), ('_F_m7', 'Fm7'), ('_F_maj7', 'FΔ'), ('_F_6', 'F6'), ('_F_m7b5', 'Fm7b5'), ('_F_dim', 'Fo'))), ('E', (('_E_', 'E'), ('_E_m', 'Em'), ('_E_7', 'E7'), ('_E_m7', 'Em7'), ('_E_maj7', 'EΔ'), ('_E_6', 'E6'), ('_E_m7b5', 'Em7b5'), ('_E_dim', 'Eo'))), ('Eb', (('_Eb_', 'Eb'), ('_Eb_m', 'Ebm'), ('_Eb_7', 'Eb7'), ('_Eb_m7', 'Ebm7'), ('_Eb_maj7', 'EbΔ'), ('_Eb_6', 'Eb6'), ('_Eb_m7b5', 'Ebm7b5'), ('_Eb_dim', 'Ebo'))), ('D', (('_D_', 'D'), ('_D_m', 'Dm'), ('_D_7', 'D7'), ('_D_m7', 'Dm7'), ('_D_maj7', 'DΔ'), ('_D_6', 'D6'), ('_D_m7b5', 'Dm7b5'), ('_D_dim', 'Do'))), ('Db', (('_Db_', 'Db'), ('_Db_m', 'Dbm'), ('_Db_7', 'Db7'), ('_Db_m7', 'Dbm7'), ('_Db_maj7', 'DbΔ'), ('_Db_6', 'Db6'), ('_Db_m7b5', 'Dbm7b5'), ('_Db_dim', 'Dbo')))], default='-', max_length=10)),
                ('m1_b3', models.CharField(choices=[('.', '-'), ('C', (('_C_', 'C'), ('_C_m', 'Cm'), ('_C_7', 'C7'), ('_C_m7', 'Cm7'), ('_C_maj7', 'CΔ'), ('_C_6', 'C6'), ('_C_m7b5', 'Cm7b5'), ('_C_dim', 'Co'))), ('B', (('_B_', 'B'), ('_B_m', 'Bm'), ('_B_7', 'B7'), ('_B_m7', 'Bm7'), ('_B_maj7', 'BΔ'), ('_B_6', 'B6'), ('_B_m7b5', 'Bm7b5'), ('_B_dim', 'Bo'))), ('Bb', (('_Bb_', 'Bb'), ('_Bb_m', 'Bbm'), ('_Bb_7', 'Bb7'), ('_Bb_m7', 'Bbm7'), ('_Bb_maj7', 'BbΔ'), ('_Bb_6', 'Bb6'), ('_Bb_m7b5', 'Bbm7b5'), ('_Bb_dim', 'Bbo'))), ('A', (('_A_', 'A'), ('_A_m', 'Am'), ('_A_7', 'A7'), ('_A_m7', 'Am7'), ('_A_maj7', 'AΔ'), ('_A_6', 'A6'), ('_A_m7b5', 'Am7b5'), ('_A_dim', 'Ao'))), ('Ab', (('_Ab_', 'Ab'), ('_Ab_m', 'Abm'), ('_Ab_7', 'Ab7'), ('_Ab_m7', 'Abm7'), ('_Ab_maj7', 'AbΔ'), ('_Ab_6', 'Ab6'), ('_Ab_m7b5', 'Abm7b5'), ('_Ab_dim', 'Abo'))), ('G', (('_G_', 'G'), ('_G_m', 'Gm'), ('_G_7', 'G7'), ('_G_m7', 'Gm7'), ('_G_maj7', 'GΔ'), ('_G_6', 'G6'), ('_G_m7b5', 'Gm7b5'), ('_G_dim', 'Go'))), ('Gb', (('_Gb_', 'Gb'), ('_Gb_m', 'Gbm'), ('_Gb_7', 'Gb7'), ('_Gb_m7', 'Gbm7'), ('_Gb_maj7', 'GbΔ'), ('_Gb_6', 'Gb6'), ('_Gb_m7b5', 'Gbm7b5'), ('_Gb_dim', 'Gbo'))), ('F', (('_F_', 'F'), ('_F_m', 'Fm'), ('_F_7', 'F7'), ('_F_m7', 'Fm7'), ('_F_maj7', 'FΔ'), ('_F_6', 'F6'), ('_F_m7b5', 'Fm7b5'), ('_F_dim', 'Fo'))), ('E', (('_E_', 'E'), ('_E_m', 'Em'), ('_E_7', 'E7'), ('_E_m7', 'Em7'), ('_E_maj7', 'EΔ'), ('_E_6', 'E6'), ('_E_m7b5', 'Em7b5'), ('_E_dim', 'Eo'))), ('Eb', (('_Eb_', 'Eb'), ('_Eb_m', 'Ebm'), ('_Eb_7', 'Eb7'), ('_Eb_m7', 'Ebm7'), ('_Eb_maj7', 'EbΔ'), ('_Eb_6', 'Eb6'), ('_Eb_m7b5', 'Ebm7b5'), ('_Eb_dim', 'Ebo'))), ('D', (('_D_', 'D'), ('_D_m', 'Dm'), ('_D_7', 'D7'), ('_D_m7', 'Dm7'), ('_D_maj7', 'DΔ'), ('_D_6', 'D6'), ('_D_m7b5', 'Dm7b5'), ('_D_dim', 'Do'))), ('Db', (('_Db_', 'Db'), ('_Db_m', 'Dbm'), ('_Db_7', 'Db7'), ('_Db_m7', 'Dbm7'), ('_Db_maj7', 'DbΔ'), ('_Db_6', 'Db6'), ('_Db_m7b5', 'Dbm7b5'), ('_Db_dim', 'Dbo')))], default='-', max_length=10)),
                ('m1_b4', models.CharField(choices=[('.', '-'), ('C', (('_C_', 'C'), ('_C_m', 'Cm'), ('_C_7', 'C7'), ('_C_m7', 'Cm7'), ('_C_maj7', 'CΔ'), ('_C_6', 'C6'), ('_C_m7b5', 'Cm7b5'), ('_C_dim', 'Co'))), ('B', (('_B_', 'B'), ('_B_m', 'Bm'), ('_B_7', 'B7'), ('_B_m7', 'Bm7'), ('_B_maj7', 'BΔ'), ('_B_6', 'B6'), ('_B_m7b5', 'Bm7b5'), ('_B_dim', 'Bo'))), ('Bb', (('_Bb_', 'Bb'), ('_Bb_m', 'Bbm'), ('_Bb_7', 'Bb7'), ('_Bb_m7', 'Bbm7'), ('_Bb_maj7', 'BbΔ'), ('_Bb_6', 'Bb6'), ('_Bb_m7b5', 'Bbm7b5'), ('_Bb_dim', 'Bbo'))), ('A', (('_A_', 'A'), ('_A_m', 'Am'), ('_A_7', 'A7'), ('_A_m7', 'Am7'), ('_A_maj7', 'AΔ'), ('_A_6', 'A6'), ('_A_m7b5', 'Am7b5'), ('_A_dim', 'Ao'))), ('Ab', (('_Ab_', 'Ab'), ('_Ab_m', 'Abm'), ('_Ab_7', 'Ab7'), ('_Ab_m7', 'Abm7'), ('_Ab_maj7', 'AbΔ'), ('_Ab_6', 'Ab6'), ('_Ab_m7b5', 'Abm7b5'), ('_Ab_dim', 'Abo'))), ('G', (('_G_', 'G'), ('_G_m', 'Gm'), ('_G_7', 'G7'), ('_G_m7', 'Gm7'), ('_G_maj7', 'GΔ'), ('_G_6', 'G6'), ('_G_m7b5', 'Gm7b5'), ('_G_dim', 'Go'))), ('Gb', (('_Gb_', 'Gb'), ('_Gb_m', 'Gbm'), ('_Gb_7', 'Gb7'), ('_Gb_m7', 'Gbm7'), ('_Gb_maj7', 'GbΔ'), ('_Gb_6', 'Gb6'), ('_Gb_m7b5', 'Gbm7b5'), ('_Gb_dim', 'Gbo'))), ('F', (('_F_', 'F'), ('_F_m', 'Fm'), ('_F_7', 'F7'), ('_F_m7', 'Fm7'), ('_F_maj7', 'FΔ'), ('_F_6', 'F6'), ('_F_m7b5', 'Fm7b5'), ('_F_dim', 'Fo'))), ('E', (('_E_', 'E'), ('_E_m', 'Em'), ('_E_7', 'E7'), ('_E_m7', 'Em7'), ('_E_maj7', 'EΔ'), ('_E_6', 'E6'), ('_E_m7b5', 'Em7b5'), ('_E_dim', 'Eo'))), ('Eb', (('_Eb_', 'Eb'), ('_Eb_m', 'Ebm'), ('_Eb_7', 'Eb7'), ('_Eb_m7', 'Ebm7'), ('_Eb_maj7', 'EbΔ'), ('_Eb_6', 'Eb6'), ('_Eb_m7b5', 'Ebm7b5'), ('_Eb_dim', 'Ebo'))), ('D', (('_D_', 'D'), ('_D_m', 'Dm'), ('_D_7', 'D7'), ('_D_m7', 'Dm7'), ('_D_maj7', 'DΔ'), ('_D_6', 'D6'), ('_D_m7b5', 'Dm7b5'), ('_D_dim', 'Do'))), ('Db', (('_Db_', 'Db'), ('_Db_m', 'Dbm'), ('_Db_7', 'Db7'), ('_Db_m7', 'Dbm7'), ('_Db_maj7', 'DbΔ'), ('_Db_6', 'Db6'), ('_Db_m7b5', 'Dbm7b5'), ('_Db_dim', 'Dbo')))], default='-', max_length=10)),
                ('m2_b1', models.CharField(choices=[('.', '-'), ('C', (('_C_', 'C'), ('_C_m', 'Cm'), ('_C_7', 'C7'), ('_C_m7', 'Cm7'), ('_C_maj7', 'CΔ'), ('_C_6', 'C6'), ('_C_m7b5', 'Cm7b5'), ('_C_dim', 'Co'))), ('B', (('_B_', 'B'), ('_B_m', 'Bm'), ('_B_7', 'B7'), ('_B_m7', 'Bm7'), ('_B_maj7', 'BΔ'), ('_B_6', 'B6'), ('_B_m7b5', 'Bm7b5'), ('_B_dim', 'Bo'))), ('Bb', (('_Bb_', 'Bb'), ('_Bb_m', 'Bbm'), ('_Bb_7', 'Bb7'), ('_Bb_m7', 'Bbm7'), ('_Bb_maj7', 'BbΔ'), ('_Bb_6', 'Bb6'), ('_Bb_m7b5', 'Bbm7b5'), ('_Bb_dim', 'Bbo'))), ('A', (('_A_', 'A'), ('_A_m', 'Am'), ('_A_7', 'A7'), ('_A_m7', 'Am7'), ('_A_maj7', 'AΔ'), ('_A_6', 'A6'), ('_A_m7b5', 'Am7b5'), ('_A_dim', 'Ao'))), ('Ab', (('_Ab_', 'Ab'), ('_Ab_m', 'Abm'), ('_Ab_7', 'Ab7'), ('_Ab_m7', 'Abm7'), ('_Ab_maj7', 'AbΔ'), ('_Ab_6', 'Ab6'), ('_Ab_m7b5', 'Abm7b5'), ('_Ab_dim', 'Abo'))), ('G', (('_G_', 'G'), ('_G_m', 'Gm'), ('_G_7', 'G7'), ('_G_m7', 'Gm7'), ('_G_maj7', 'GΔ'), ('_G_6', 'G6'), ('_G_m7b5', 'Gm7b5'), ('_G_dim', 'Go'))), ('Gb', (('_Gb_', 'Gb'), ('_Gb_m', 'Gbm'), ('_Gb_7', 'Gb7'), ('_Gb_m7', 'Gbm7'), ('_Gb_maj7', 'GbΔ'), ('_Gb_6', 'Gb6'), ('_Gb_m7b5', 'Gbm7b5'), ('_Gb_dim', 'Gbo'))), ('F', (('_F_', 'F'), ('_F_m', 'Fm'), ('_F_7', 'F7'), ('_F_m7', 'Fm7'), ('_F_maj7', 'FΔ'), ('_F_6', 'F6'), ('_F_m7b5', 'Fm7b5'), ('_F_dim', 'Fo'))), ('E', (('_E_', 'E'), ('_E_m', 'Em'), ('_E_7', 'E7'), ('_E_m7', 'Em7'), ('_E_maj7', 'EΔ'), ('_E_6', 'E6'), ('_E_m7b5', 'Em7b5'), ('_E_dim', 'Eo'))), ('Eb', (('_Eb_', 'Eb'), ('_Eb_m', 'Ebm'), ('_Eb_7', 'Eb7'), ('_Eb_m7', 'Ebm7'), ('_Eb_maj7', 'EbΔ'), ('_Eb_6', 'Eb6'), ('_Eb_m7b5', 'Ebm7b5'), ('_Eb_dim', 'Ebo'))), ('D', (('_D_', 'D'), ('_D_m', 'Dm'), ('_D_7', 'D7'), ('_D_m7', 'Dm7'), ('_D_maj7', 'DΔ'), ('_D_6', 'D6'), ('_D_m7b5', 'Dm7b5'), ('_D_dim', 'Do'))), ('Db', (('_Db_', 'Db'), ('_Db_m', 'Dbm'), ('_Db_7', 'Db7'), ('_Db_m7', 'Dbm7'), ('_Db_maj7', 'DbΔ'), ('_Db_6', 'Db6'), ('_Db_m7b5', 'Dbm7b5'), ('_Db_dim', 'Dbo')))], default='-', max_length=10)),
                ('m2_b2', models.CharField(choices=[('.', '-'), ('C', (('_C_', 'C'), ('_C_m', 'Cm'), ('_C_7', 'C7'), ('_C_m7', 'Cm7'), ('_C_maj7', 'CΔ'), ('_C_6', 'C6'), ('_C_m7b5', 'Cm7b5'), ('_C_dim', 'Co'))), ('B', (('_B_', 'B'), ('_B_m', 'Bm'), ('_B_7', 'B7'), ('_B_m7', 'Bm7'), ('_B_maj7', 'BΔ'), ('_B_6', 'B6'), ('_B_m7b5', 'Bm7b5'), ('_B_dim', 'Bo'))), ('Bb', (('_Bb_', 'Bb'), ('_Bb_m', 'Bbm'), ('_Bb_7', 'Bb7'), ('_Bb_m7', 'Bbm7'), ('_Bb_maj7', 'BbΔ'), ('_Bb_6', 'Bb6'), ('_Bb_m7b5', 'Bbm7b5'), ('_Bb_dim', 'Bbo'))), ('A', (('_A_', 'A'), ('_A_m', 'Am'), ('_A_7', 'A7'), ('_A_m7', 'Am7'), ('_A_maj7', 'AΔ'), ('_A_6', 'A6'), ('_A_m7b5', 'Am7b5'), ('_A_dim', 'Ao'))), ('Ab', (('_Ab_', 'Ab'), ('_Ab_m', 'Abm'), ('_Ab_7', 'Ab7'), ('_Ab_m7', 'Abm7'), ('_Ab_maj7', 'AbΔ'), ('_Ab_6', 'Ab6'), ('_Ab_m7b5', 'Abm7b5'), ('_Ab_dim', 'Abo'))), ('G', (('_G_', 'G'), ('_G_m', 'Gm'), ('_G_7', 'G7'), ('_G_m7', 'Gm7'), ('_G_maj7', 'GΔ'), ('_G_6', 'G6'), ('_G_m7b5', 'Gm7b5'), ('_G_dim', 'Go'))), ('Gb', (('_Gb_', 'Gb'), ('_Gb_m', 'Gbm'), ('_Gb_7', 'Gb7'), ('_Gb_m7', 'Gbm7'), ('_Gb_maj7', 'GbΔ'), ('_Gb_6', 'Gb6'), ('_Gb_m7b5', 'Gbm7b5'), ('_Gb_dim', 'Gbo'))), ('F', (('_F_', 'F'), ('_F_m', 'Fm'), ('_F_7', 'F7'), ('_F_m7', 'Fm7'), ('_F_maj7', 'FΔ'), ('_F_6', 'F6'), ('_F_m7b5', 'Fm7b5'), ('_F_dim', 'Fo'))), ('E', (('_E_', 'E'), ('_E_m', 'Em'), ('_E_7', 'E7'), ('_E_m7', 'Em7'), ('_E_maj7', 'EΔ'), ('_E_6', 'E6'), ('_E_m7b5', 'Em7b5'), ('_E_dim', 'Eo'))), ('Eb', (('_Eb_', 'Eb'), ('_Eb_m', 'Ebm'), ('_Eb_7', 'Eb7'), ('_Eb_m7', 'Ebm7'), ('_Eb_maj7', 'EbΔ'), ('_Eb_6', 'Eb6'), ('_Eb_m7b5', 'Ebm7b5'), ('_Eb_dim', 'Ebo'))), ('D', (('_D_', 'D'), ('_D_m', 'Dm'), ('_D_7', 'D7'), ('_D_m7', 'Dm7'), ('_D_maj7', 'DΔ'), ('_D_6', 'D6'), ('_D_m7b5', 'Dm7b5'), ('_D_dim', 'Do'))), ('Db', (('_Db_', 'Db'), ('_Db_m', 'Dbm'), ('_Db_7', 'Db7'), ('_Db_m7', 'Dbm7'), ('_Db_maj7', 'DbΔ'), ('_Db_6', 'Db6'), ('_Db_m7b5', 'Dbm7b5'), ('_Db_dim', 'Dbo')))], default='-', max_length=10)),
                ('m2_b3', models.CharField(choices=[('.', '-'), ('C', (('_C_', 'C'), ('_C_m', 'Cm'), ('_C_7', 'C7'), ('_C_m7', 'Cm7'), ('_C_maj7', 'CΔ'), ('_C_6', 'C6'), ('_C_m7b5', 'Cm7b5'), ('_C_dim', 'Co'))), ('B', (('_B_', 'B'), ('_B_m', 'Bm'), ('_B_7', 'B7'), ('_B_m7', 'Bm7'), ('_B_maj7', 'BΔ'), ('_B_6', 'B6'), ('_B_m7b5', 'Bm7b5'), ('_B_dim', 'Bo'))), ('Bb', (('_Bb_', 'Bb'), ('_Bb_m', 'Bbm'), ('_Bb_7', 'Bb7'), ('_Bb_m7', 'Bbm7'), ('_Bb_maj7', 'BbΔ'), ('_Bb_6', 'Bb6'), ('_Bb_m7b5', 'Bbm7b5'), ('_Bb_dim', 'Bbo'))), ('A', (('_A_', 'A'), ('_A_m', 'Am'), ('_A_7', 'A7'), ('_A_m7', 'Am7'), ('_A_maj7', 'AΔ'), ('_A_6', 'A6'), ('_A_m7b5', 'Am7b5'), ('_A_dim', 'Ao'))), ('Ab', (('_Ab_', 'Ab'), ('_Ab_m', 'Abm'), ('_Ab_7', 'Ab7'), ('_Ab_m7', 'Abm7'), ('_Ab_maj7', 'AbΔ'), ('_Ab_6', 'Ab6'), ('_Ab_m7b5', 'Abm7b5'), ('_Ab_dim', 'Abo'))), ('G', (('_G_', 'G'), ('_G_m', 'Gm'), ('_G_7', 'G7'), ('_G_m7', 'Gm7'), ('_G_maj7', 'GΔ'), ('_G_6', 'G6'), ('_G_m7b5', 'Gm7b5'), ('_G_dim', 'Go'))), ('Gb', (('_Gb_', 'Gb'), ('_Gb_m', 'Gbm'), ('_Gb_7', 'Gb7'), ('_Gb_m7', 'Gbm7'), ('_Gb_maj7', 'GbΔ'), ('_Gb_6', 'Gb6'), ('_Gb_m7b5', 'Gbm7b5'), ('_Gb_dim', 'Gbo'))), ('F', (('_F_', 'F'), ('_F_m', 'Fm'), ('_F_7', 'F7'), ('_F_m7', 'Fm7'), ('_F_maj7', 'FΔ'), ('_F_6', 'F6'), ('_F_m7b5', 'Fm7b5'), ('_F_dim', 'Fo'))), ('E', (('_E_', 'E'), ('_E_m', 'Em'), ('_E_7', 'E7'), ('_E_m7', 'Em7'), ('_E_maj7', 'EΔ'), ('_E_6', 'E6'), ('_E_m7b5', 'Em7b5'), ('_E_dim', 'Eo'))), ('Eb', (('_Eb_', 'Eb'), ('_Eb_m', 'Ebm'), ('_Eb_7', 'Eb7'), ('_Eb_m7', 'Ebm7'), ('_Eb_maj7', 'EbΔ'), ('_Eb_6', 'Eb6'), ('_Eb_m7b5', 'Ebm7b5'), ('_Eb_dim', 'Ebo'))), ('D', (('_D_', 'D'), ('_D_m', 'Dm'), ('_D_7', 'D7'), ('_D_m7', 'Dm7'), ('_D_maj7', 'DΔ'), ('_D_6', 'D6'), ('_D_m7b5', 'Dm7b5'), ('_D_dim', 'Do'))), ('Db', (('_Db_', 'Db'), ('_Db_m', 'Dbm'), ('_Db_7', 'Db7'), ('_Db_m7', 'Dbm7'), ('_Db_maj7', 'DbΔ'), ('_Db_6', 'Db6'), ('_Db_m7b5', 'Dbm7b5'), ('_Db_dim', 'Dbo')))], default='-', max_length=10)),
                ('m2_b4', models.CharField(choices=[('.', '-'), ('C', (('_C_', 'C'), ('_C_m', 'Cm'), ('_C_7', 'C7'), ('_C_m7', 'Cm7'), ('_C_maj7', 'CΔ'), ('_C_6', 'C6'), ('_C_m7b5', 'Cm7b5'), ('_C_dim', 'Co'))), ('B', (('_B_', 'B'), ('_B_m', 'Bm'), ('_B_7', 'B7'), ('_B_m7', 'Bm7'), ('_B_maj7', 'BΔ'), ('_B_6', 'B6'), ('_B_m7b5', 'Bm7b5'), ('_B_dim', 'Bo'))), ('Bb', (('_Bb_', 'Bb'), ('_Bb_m', 'Bbm'), ('_Bb_7', 'Bb7'), ('_Bb_m7', 'Bbm7'), ('_Bb_maj7', 'BbΔ'), ('_Bb_6', 'Bb6'), ('_Bb_m7b5', 'Bbm7b5'), ('_Bb_dim', 'Bbo'))), ('A', (('_A_', 'A'), ('_A_m', 'Am'), ('_A_7', 'A7'), ('_A_m7', 'Am7'), ('_A_maj7', 'AΔ'), ('_A_6', 'A6'), ('_A_m7b5', 'Am7b5'), ('_A_dim', 'Ao'))), ('Ab', (('_Ab_', 'Ab'), ('_Ab_m', 'Abm'), ('_Ab_7', 'Ab7'), ('_Ab_m7', 'Abm7'), ('_Ab_maj7', 'AbΔ'), ('_Ab_6', 'Ab6'), ('_Ab_m7b5', 'Abm7b5'), ('_Ab_dim', 'Abo'))), ('G', (('_G_', 'G'), ('_G_m', 'Gm'), ('_G_7', 'G7'), ('_G_m7', 'Gm7'), ('_G_maj7', 'GΔ'), ('_G_6', 'G6'), ('_G_m7b5', 'Gm7b5'), ('_G_dim', 'Go'))), ('Gb', (('_Gb_', 'Gb'), ('_Gb_m', 'Gbm'), ('_Gb_7', 'Gb7'), ('_Gb_m7', 'Gbm7'), ('_Gb_maj7', 'GbΔ'), ('_Gb_6', 'Gb6'), ('_Gb_m7b5', 'Gbm7b5'), ('_Gb_dim', 'Gbo'))), ('F', (('_F_', 'F'), ('_F_m', 'Fm'), ('_F_7', 'F7'), ('_F_m7', 'Fm7'), ('_F_maj7', 'FΔ'), ('_F_6', 'F6'), ('_F_m7b5', 'Fm7b5'), ('_F_dim', 'Fo'))), ('E', (('_E_', 'E'), ('_E_m', 'Em'), ('_E_7', 'E7'), ('_E_m7', 'Em7'), ('_E_maj7', 'EΔ'), ('_E_6', 'E6'), ('_E_m7b5', 'Em7b5'), ('_E_dim', 'Eo'))), ('Eb', (('_Eb_', 'Eb'), ('_Eb_m', 'Ebm'), ('_Eb_7', 'Eb7'), ('_Eb_m7', 'Ebm7'), ('_Eb_maj7', 'EbΔ'), ('_Eb_6', 'Eb6'), ('_Eb_m7b5', 'Ebm7b5'), ('_Eb_dim', 'Ebo'))), ('D', (('_D_', 'D'), ('_D_m', 'Dm'), ('_D_7', 'D7'), ('_D_m7', 'Dm7'), ('_D_maj7', 'DΔ'), ('_D_6', 'D6'), ('_D_m7b5', 'Dm7b5'), ('_D_dim', 'Do'))), ('Db', (('_Db_', 'Db'), ('_Db_m', 'Dbm'), ('_Db_7', 'Db7'), ('_Db_m7', 'Dbm7'), ('_Db_maj7', 'DbΔ'), ('_Db_6', 'Db6'), ('_Db_m7b5', 'Dbm7b5'), ('_Db_dim', 'Dbo')))], default='-', max_length=10)),
                ('m3_b1', models.CharField(choices=[('.', '-'), ('C', (('_C_', 'C'), ('_C_m', 'Cm'), ('_C_7', 'C7'), ('_C_m7', 'Cm7'), ('_C_maj7', 'CΔ'), ('_C_6', 'C6'), ('_C_m7b5', 'Cm7b5'), ('_C_dim', 'Co'))), ('B', (('_B_', 'B'), ('_B_m', 'Bm'), ('_B_7', 'B7'), ('_B_m7', 'Bm7'), ('_B_maj7', 'BΔ'), ('_B_6', 'B6'), ('_B_m7b5', 'Bm7b5'), ('_B_dim', 'Bo'))), ('Bb', (('_Bb_', 'Bb'), ('_Bb_m', 'Bbm'), ('_Bb_7', 'Bb7'), ('_Bb_m7', 'Bbm7'), ('_Bb_maj7', 'BbΔ'), ('_Bb_6', 'Bb6'), ('_Bb_m7b5', 'Bbm7b5'), ('_Bb_dim', 'Bbo'))), ('A', (('_A_', 'A'), ('_A_m', 'Am'), ('_A_7', 'A7'), ('_A_m7', 'Am7'), ('_A_maj7', 'AΔ'), ('_A_6', 'A6'), ('_A_m7b5', 'Am7b5'), ('_A_dim', 'Ao'))), ('Ab', (('_Ab_', 'Ab'), ('_Ab_m', 'Abm'), ('_Ab_7', 'Ab7'), ('_Ab_m7', 'Abm7'), ('_Ab_maj7', 'AbΔ'), ('_Ab_6', 'Ab6'), ('_Ab_m7b5', 'Abm7b5'), ('_Ab_dim', 'Abo'))), ('G', (('_G_', 'G'), ('_G_m', 'Gm'), ('_G_7', 'G7'), ('_G_m7', 'Gm7'), ('_G_maj7', 'GΔ'), ('_G_6', 'G6'), ('_G_m7b5', 'Gm7b5'), ('_G_dim', 'Go'))), ('Gb', (('_Gb_', 'Gb'), ('_Gb_m', 'Gbm'), ('_Gb_7', 'Gb7'), ('_Gb_m7', 'Gbm7'), ('_Gb_maj7', 'GbΔ'), ('_Gb_6', 'Gb6'), ('_Gb_m7b5', 'Gbm7b5'), ('_Gb_dim', 'Gbo'))), ('F', (('_F_', 'F'), ('_F_m', 'Fm'), ('_F_7', 'F7'), ('_F_m7', 'Fm7'), ('_F_maj7', 'FΔ'), ('_F_6', 'F6'), ('_F_m7b5', 'Fm7b5'), ('_F_dim', 'Fo'))), ('E', (('_E_', 'E'), ('_E_m', 'Em'), ('_E_7', 'E7'), ('_E_m7', 'Em7'), ('_E_maj7', 'EΔ'), ('_E_6', 'E6'), ('_E_m7b5', 'Em7b5'), ('_E_dim', 'Eo'))), ('Eb', (('_Eb_', 'Eb'), ('_Eb_m', 'Ebm'), ('_Eb_7', 'Eb7'), ('_Eb_m7', 'Ebm7'), ('_Eb_maj7', 'EbΔ'), ('_Eb_6', 'Eb6'), ('_Eb_m7b5', 'Ebm7b5'), ('_Eb_dim', 'Ebo'))), ('D', (('_D_', 'D'), ('_D_m', 'Dm'), ('_D_7', 'D7'), ('_D_m7', 'Dm7'), ('_D_maj7', 'DΔ'), ('_D_6', 'D6'), ('_D_m7b5', 'Dm7b5'), ('_D_dim', 'Do'))), ('Db', (('_Db_', 'Db'), ('_Db_m', 'Dbm'), ('_Db_7', 'Db7'), ('_Db_m7', 'Dbm7'), ('_Db_maj7', 'DbΔ'), ('_Db_6', 'Db6'), ('_Db_m7b5', 'Dbm7b5'), ('_Db_dim', 'Dbo')))], default='-', max_length=10)),
                ('m3_b2', models.CharField(choices=[('.', '-'), ('C', (('_C_', 'C'), ('_C_m', 'Cm'), ('_C_7', 'C7'), ('_C_m7', 'Cm7'), ('_C_maj7', 'CΔ'), ('_C_6', 'C6'), ('_C_m7b5', 'Cm7b5'), ('_C_dim', 'Co'))), ('B', (('_B_', 'B'), ('_B_m', 'Bm'), ('_B_7', 'B7'), ('_B_m7', 'Bm7'), ('_B_maj7', 'BΔ'), ('_B_6', 'B6'), ('_B_m7b5', 'Bm7b5'), ('_B_dim', 'Bo'))), ('Bb', (('_Bb_', 'Bb'), ('_Bb_m', 'Bbm'), ('_Bb_7', 'Bb7'), ('_Bb_m7', 'Bbm7'), ('_Bb_maj7', 'BbΔ'), ('_Bb_6', 'Bb6'), ('_Bb_m7b5', 'Bbm7b5'), ('_Bb_dim', 'Bbo'))), ('A', (('_A_', 'A'), ('_A_m', 'Am'), ('_A_7', 'A7'), ('_A_m7', 'Am7'), ('_A_maj7', 'AΔ'), ('_A_6', 'A6'), ('_A_m7b5', 'Am7b5'), ('_A_dim', 'Ao'))), ('Ab', (('_Ab_', 'Ab'), ('_Ab_m', 'Abm'), ('_Ab_7', 'Ab7'), ('_Ab_m7', 'Abm7'), ('_Ab_maj7', 'AbΔ'), ('_Ab_6', 'Ab6'), ('_Ab_m7b5', 'Abm7b5'), ('_Ab_dim', 'Abo'))), ('G', (('_G_', 'G'), ('_G_m', 'Gm'), ('_G_7', 'G7'), ('_G_m7', 'Gm7'), ('_G_maj7', 'GΔ'), ('_G_6', 'G6'), ('_G_m7b5', 'Gm7b5'), ('_G_dim', 'Go'))), ('Gb', (('_Gb_', 'Gb'), ('_Gb_m', 'Gbm'), ('_Gb_7', 'Gb7'), ('_Gb_m7', 'Gbm7'), ('_Gb_maj7', 'GbΔ'), ('_Gb_6', 'Gb6'), ('_Gb_m7b5', 'Gbm7b5'), ('_Gb_dim', 'Gbo'))), ('F', (('_F_', 'F'), ('_F_m', 'Fm'), ('_F_7', 'F7'), ('_F_m7', 'Fm7'), ('_F_maj7', 'FΔ'), ('_F_6', 'F6'), ('_F_m7b5', 'Fm7b5'), ('_F_dim', 'Fo'))), ('E', (('_E_', 'E'), ('_E_m', 'Em'), ('_E_7', 'E7'), ('_E_m7', 'Em7'), ('_E_maj7', 'EΔ'), ('_E_6', 'E6'), ('_E_m7b5', 'Em7b5'), ('_E_dim', 'Eo'))), ('Eb', (('_Eb_', 'Eb'), ('_Eb_m', 'Ebm'), ('_Eb_7', 'Eb7'), ('_Eb_m7', 'Ebm7'), ('_Eb_maj7', 'EbΔ'), ('_Eb_6', 'Eb6'), ('_Eb_m7b5', 'Ebm7b5'), ('_Eb_dim', 'Ebo'))), ('D', (('_D_', 'D'), ('_D_m', 'Dm'), ('_D_7', 'D7'), ('_D_m7', 'Dm7'), ('_D_maj7', 'DΔ'), ('_D_6', 'D6'), ('_D_m7b5', 'Dm7b5'), ('_D_dim', 'Do'))), ('Db', (('_Db_', 'Db'), ('_Db_m', 'Dbm'), ('_Db_7', 'Db7'), ('_Db_m7', 'Dbm7'), ('_Db_maj7', 'DbΔ'), ('_Db_6', 'Db6'), ('_Db_m7b5', 'Dbm7b5'), ('_Db_dim', 'Dbo')))], default='-', max_length=10)),
                ('m3_b3', models.CharField(choices=[('.', '-'), ('C', (('_C_', 'C'), ('_C_m', 'Cm'), ('_C_7', 'C7'), ('_C_m7', 'Cm7'), ('_C_maj7', 'CΔ'), ('_C_6', 'C6'), ('_C_m7b5', 'Cm7b5'), ('_C_dim', 'Co'))), ('B', (('_B_', 'B'), ('_B_m', 'Bm'), ('_B_7', 'B7'), ('_B_m7', 'Bm7'), ('_B_maj7', 'BΔ'), ('_B_6', 'B6'), ('_B_m7b5', 'Bm7b5'), ('_B_dim', 'Bo'))), ('Bb', (('_Bb_', 'Bb'), ('_Bb_m', 'Bbm'), ('_Bb_7', 'Bb7'), ('_Bb_m7', 'Bbm7'), ('_Bb_maj7', 'BbΔ'), ('_Bb_6', 'Bb6'), ('_Bb_m7b5', 'Bbm7b5'), ('_Bb_dim', 'Bbo'))), ('A', (('_A_', 'A'), ('_A_m', 'Am'), ('_A_7', 'A7'), ('_A_m7', 'Am7'), ('_A_maj7', 'AΔ'), ('_A_6', 'A6'), ('_A_m7b5', 'Am7b5'), ('_A_dim', 'Ao'))), ('Ab', (('_Ab_', 'Ab'), ('_Ab_m', 'Abm'), ('_Ab_7', 'Ab7'), ('_Ab_m7', 'Abm7'), ('_Ab_maj7', 'AbΔ'), ('_Ab_6', 'Ab6'), ('_Ab_m7b5', 'Abm7b5'), ('_Ab_dim', 'Abo'))), ('G', (('_G_', 'G'), ('_G_m', 'Gm'), ('_G_7', 'G7'), ('_G_m7', 'Gm7'), ('_G_maj7', 'GΔ'), ('_G_6', 'G6'), ('_G_m7b5', 'Gm7b5'), ('_G_dim', 'Go'))), ('Gb', (('_Gb_', 'Gb'), ('_Gb_m', 'Gbm'), ('_Gb_7', 'Gb7'), ('_Gb_m7', 'Gbm7'), ('_Gb_maj7', 'GbΔ'), ('_Gb_6', 'Gb6'), ('_Gb_m7b5', 'Gbm7b5'), ('_Gb_dim', 'Gbo'))), ('F', (('_F_', 'F'), ('_F_m', 'Fm'), ('_F_7', 'F7'), ('_F_m7', 'Fm7'), ('_F_maj7', 'FΔ'), ('_F_6', 'F6'), ('_F_m7b5', 'Fm7b5'), ('_F_dim', 'Fo'))), ('E', (('_E_', 'E'), ('_E_m', 'Em'), ('_E_7', 'E7'), ('_E_m7', 'Em7'), ('_E_maj7', 'EΔ'), ('_E_6', 'E6'), ('_E_m7b5', 'Em7b5'), ('_E_dim', 'Eo'))), ('Eb', (('_Eb_', 'Eb'), ('_Eb_m', 'Ebm'), ('_Eb_7', 'Eb7'), ('_Eb_m7', 'Ebm7'), ('_Eb_maj7', 'EbΔ'), ('_Eb_6', 'Eb6'), ('_Eb_m7b5', 'Ebm7b5'), ('_Eb_dim', 'Ebo'))), ('D', (('_D_', 'D'), ('_D_m', 'Dm'), ('_D_7', 'D7'), ('_D_m7', 'Dm7'), ('_D_maj7', 'DΔ'), ('_D_6', 'D6'), ('_D_m7b5', 'Dm7b5'), ('_D_dim', 'Do'))), ('Db', (('_Db_', 'Db'), ('_Db_m', 'Dbm'), ('_Db_7', 'Db7'), ('_Db_m7', 'Dbm7'), ('_Db_maj7', 'DbΔ'), ('_Db_6', 'Db6'), ('_Db_m7b5', 'Dbm7b5'), ('_Db_dim', 'Dbo')))], default='-', max_length=10)),
                ('m3_b4', models.CharField(choices=[('.', '-'), ('C', (('_C_', 'C'), ('_C_m', 'Cm'), ('_C_7', 'C7'), ('_C_m7', 'Cm7'), ('_C_maj7', 'CΔ'), ('_C_6', 'C6'), ('_C_m7b5', 'Cm7b5'), ('_C_dim', 'Co'))), ('B', (('_B_', 'B'), ('_B_m', 'Bm'), ('_B_7', 'B7'), ('_B_m7', 'Bm7'), ('_B_maj7', 'BΔ'), ('_B_6', 'B6'), ('_B_m7b5', 'Bm7b5'), ('_B_dim', 'Bo'))), ('Bb', (('_Bb_', 'Bb'), ('_Bb_m', 'Bbm'), ('_Bb_7', 'Bb7'), ('_Bb_m7', 'Bbm7'), ('_Bb_maj7', 'BbΔ'), ('_Bb_6', 'Bb6'), ('_Bb_m7b5', 'Bbm7b5'), ('_Bb_dim', 'Bbo'))), ('A', (('_A_', 'A'), ('_A_m', 'Am'), ('_A_7', 'A7'), ('_A_m7', 'Am7'), ('_A_maj7', 'AΔ'), ('_A_6', 'A6'), ('_A_m7b5', 'Am7b5'), ('_A_dim', 'Ao'))), ('Ab', (('_Ab_', 'Ab'), ('_Ab_m', 'Abm'), ('_Ab_7', 'Ab7'), ('_Ab_m7', 'Abm7'), ('_Ab_maj7', 'AbΔ'), ('_Ab_6', 'Ab6'), ('_Ab_m7b5', 'Abm7b5'), ('_Ab_dim', 'Abo'))), ('G', (('_G_', 'G'), ('_G_m', 'Gm'), ('_G_7', 'G7'), ('_G_m7', 'Gm7'), ('_G_maj7', 'GΔ'), ('_G_6', 'G6'), ('_G_m7b5', 'Gm7b5'), ('_G_dim', 'Go'))), ('Gb', (('_Gb_', 'Gb'), ('_Gb_m', 'Gbm'), ('_Gb_7', 'Gb7'), ('_Gb_m7', 'Gbm7'), ('_Gb_maj7', 'GbΔ'), ('_Gb_6', 'Gb6'), ('_Gb_m7b5', 'Gbm7b5'), ('_Gb_dim', 'Gbo'))), ('F', (('_F_', 'F'), ('_F_m', 'Fm'), ('_F_7', 'F7'), ('_F_m7', 'Fm7'), ('_F_maj7', 'FΔ'), ('_F_6', 'F6'), ('_F_m7b5', 'Fm7b5'), ('_F_dim', 'Fo'))), ('E', (('_E_', 'E'), ('_E_m', 'Em'), ('_E_7', 'E7'), ('_E_m7', 'Em7'), ('_E_maj7', 'EΔ'), ('_E_6', 'E6'), ('_E_m7b5', 'Em7b5'), ('_E_dim', 'Eo'))), ('Eb', (('_Eb_', 'Eb'), ('_Eb_m', 'Ebm'), ('_Eb_7', 'Eb7'), ('_Eb_m7', 'Ebm7'), ('_Eb_maj7', 'EbΔ'), ('_Eb_6', 'Eb6'), ('_Eb_m7b5', 'Ebm7b5'), ('_Eb_dim', 'Ebo'))), ('D', (('_D_', 'D'), ('_D_m', 'Dm'), ('_D_7', 'D7'), ('_D_m7', 'Dm7'), ('_D_maj7', 'DΔ'), ('_D_6', 'D6'), ('_D_m7b5', 'Dm7b5'), ('_D_dim', 'Do'))), ('Db', (('_Db_', 'Db'), ('_Db_m', 'Dbm'), ('_Db_7', 'Db7'), ('_Db_m7', 'Dbm7'), ('_Db_maj7', 'DbΔ'), ('_Db_6', 'Db6'), ('_Db_m7b5', 'Dbm7b5'), ('_Db_dim', 'Dbo')))], default='-', max_length=10)),
                ('m4_b1', models.CharField(choices=[('.', '-'), ('C', (('_C_', 'C'), ('_C_m', 'Cm'), ('_C_7', 'C7'), ('_C_m7', 'Cm7'), ('_C_maj7', 'CΔ'), ('_C_6', 'C6'), ('_C_m7b5', 'Cm7b5'), ('_C_dim', 'Co'))), ('B', (('_B_', 'B'), ('_B_m', 'Bm'), ('_B_7', 'B7'), ('_B_m7', 'Bm7'), ('_B_maj7', 'BΔ'), ('_B_6', 'B6'), ('_B_m7b5', 'Bm7b5'), ('_B_dim', 'Bo'))), ('Bb', (('_Bb_', 'Bb'), ('_Bb_m', 'Bbm'), ('_Bb_7', 'Bb7'), ('_Bb_m7', 'Bbm7'), ('_Bb_maj7', 'BbΔ'), ('_Bb_6', 'Bb6'), ('_Bb_m7b5', 'Bbm7b5'), ('_Bb_dim', 'Bbo'))), ('A', (('_A_', 'A'), ('_A_m', 'Am'), ('_A_7', 'A7'), ('_A_m7', 'Am7'), ('_A_maj7', 'AΔ'), ('_A_6', 'A6'), ('_A_m7b5', 'Am7b5'), ('_A_dim', 'Ao'))), ('Ab', (('_Ab_', 'Ab'), ('_Ab_m', 'Abm'), ('_Ab_7', 'Ab7'), ('_Ab_m7', 'Abm7'), ('_Ab_maj7', 'AbΔ'), ('_Ab_6', 'Ab6'), ('_Ab_m7b5', 'Abm7b5'), ('_Ab_dim', 'Abo'))), ('G', (('_G_', 'G'), ('_G_m', 'Gm'), ('_G_7', 'G7'), ('_G_m7', 'Gm7'), ('_G_maj7', 'GΔ'), ('_G_6', 'G6'), ('_G_m7b5', 'Gm7b5'), ('_G_dim', 'Go'))), ('Gb', (('_Gb_', 'Gb'), ('_Gb_m', 'Gbm'), ('_Gb_7', 'Gb7'), ('_Gb_m7', 'Gbm7'), ('_Gb_maj7', 'GbΔ'), ('_Gb_6', 'Gb6'), ('_Gb_m7b5', 'Gbm7b5'), ('_Gb_dim', 'Gbo'))), ('F', (('_F_', 'F'), ('_F_m', 'Fm'), ('_F_7', 'F7'), ('_F_m7', 'Fm7'), ('_F_maj7', 'FΔ'), ('_F_6', 'F6'), ('_F_m7b5', 'Fm7b5'), ('_F_dim', 'Fo'))), ('E', (('_E_', 'E'), ('_E_m', 'Em'), ('_E_7', 'E7'), ('_E_m7', 'Em7'), ('_E_maj7', 'EΔ'), ('_E_6', 'E6'), ('_E_m7b5', 'Em7b5'), ('_E_dim', 'Eo'))), ('Eb', (('_Eb_', 'Eb'), ('_Eb_m', 'Ebm'), ('_Eb_7', 'Eb7'), ('_Eb_m7', 'Ebm7'), ('_Eb_maj7', 'EbΔ'), ('_Eb_6', 'Eb6'), ('_Eb_m7b5', 'Ebm7b5'), ('_Eb_dim', 'Ebo'))), ('D', (('_D_', 'D'), ('_D_m', 'Dm'), ('_D_7', 'D7'), ('_D_m7', 'Dm7'), ('_D_maj7', 'DΔ'), ('_D_6', 'D6'), ('_D_m7b5', 'Dm7b5'), ('_D_dim', 'Do'))), ('Db', (('_Db_', 'Db'), ('_Db_m', 'Dbm'), ('_Db_7', 'Db7'), ('_Db_m7', 'Dbm7'), ('_Db_maj7', 'DbΔ'), ('_Db_6', 'Db6'), ('_Db_m7b5', 'Dbm7b5'), ('_Db_dim', 'Dbo')))], default='-', max_length=10)),
                ('m4_b2', models.CharField(choices=[('.', '-'), ('C', (('_C_', 'C'), ('_C_m', 'Cm'), ('_C_7', 'C7'), ('_C_m7', 'Cm7'), ('_C_maj7', 'CΔ'), ('_C_6', 'C6'), ('_C_m7b5', 'Cm7b5'), ('_C_dim', 'Co'))), ('B', (('_B_', 'B'), ('_B_m', 'Bm'), ('_B_7', 'B7'), ('_B_m7', 'Bm7'), ('_B_maj7', 'BΔ'), ('_B_6', 'B6'), ('_B_m7b5', 'Bm7b5'), ('_B_dim', 'Bo'))), ('Bb', (('_Bb_', 'Bb'), ('_Bb_m', 'Bbm'), ('_Bb_7', 'Bb7'), ('_Bb_m7', 'Bbm7'), ('_Bb_maj7', 'BbΔ'), ('_Bb_6', 'Bb6'), ('_Bb_m7b5', 'Bbm7b5'), ('_Bb_dim', 'Bbo'))), ('A', (('_A_', 'A'), ('_A_m', 'Am'), ('_A_7', 'A7'), ('_A_m7', 'Am7'), ('_A_maj7', 'AΔ'), ('_A_6', 'A6'), ('_A_m7b5', 'Am7b5'), ('_A_dim', 'Ao'))), ('Ab', (('_Ab_', 'Ab'), ('_Ab_m', 'Abm'), ('_Ab_7', 'Ab7'), ('_Ab_m7', 'Abm7'), ('_Ab_maj7', 'AbΔ'), ('_Ab_6', 'Ab6'), ('_Ab_m7b5', 'Abm7b5'), ('_Ab_dim', 'Abo'))), ('G', (('_G_', 'G'), ('_G_m', 'Gm'), ('_G_7', 'G7'), ('_G_m7', 'Gm7'), ('_G_maj7', 'GΔ'), ('_G_6', 'G6'), ('_G_m7b5', 'Gm7b5'), ('_G_dim', 'Go'))), ('Gb', (('_Gb_', 'Gb'), ('_Gb_m', 'Gbm'), ('_Gb_7', 'Gb7'), ('_Gb_m7', 'Gbm7'), ('_Gb_maj7', 'GbΔ'), ('_Gb_6', 'Gb6'), ('_Gb_m7b5', 'Gbm7b5'), ('_Gb_dim', 'Gbo'))), ('F', (('_F_', 'F'), ('_F_m', 'Fm'), ('_F_7', 'F7'), ('_F_m7', 'Fm7'), ('_F_maj7', 'FΔ'), ('_F_6', 'F6'), ('_F_m7b5', 'Fm7b5'), ('_F_dim', 'Fo'))), ('E', (('_E_', 'E'), ('_E_m', 'Em'), ('_E_7', 'E7'), ('_E_m7', 'Em7'), ('_E_maj7', 'EΔ'), ('_E_6', 'E6'), ('_E_m7b5', 'Em7b5'), ('_E_dim', 'Eo'))), ('Eb', (('_Eb_', 'Eb'), ('_Eb_m', 'Ebm'), ('_Eb_7', 'Eb7'), ('_Eb_m7', 'Ebm7'), ('_Eb_maj7', 'EbΔ'), ('_Eb_6', 'Eb6'), ('_Eb_m7b5', 'Ebm7b5'), ('_Eb_dim', 'Ebo'))), ('D', (('_D_', 'D'), ('_D_m', 'Dm'), ('_D_7', 'D7'), ('_D_m7', 'Dm7'), ('_D_maj7', 'DΔ'), ('_D_6', 'D6'), ('_D_m7b5', 'Dm7b5'), ('_D_dim', 'Do'))), ('Db', (('_Db_', 'Db'), ('_Db_m', 'Dbm'), ('_Db_7', 'Db7'), ('_Db_m7', 'Dbm7'), ('_Db_maj7', 'DbΔ'), ('_Db_6', 'Db6'), ('_Db_m7b5', 'Dbm7b5'), ('_Db_dim', 'Dbo')))], default='-', max_length=10)),
                ('m4_b3', models.CharField(choices=[('.', '-'), ('C', (('_C_', 'C'), ('_C_m', 'Cm'), ('_C_7', 'C7'), ('_C_m7', 'Cm7'), ('_C_maj7', 'CΔ'), ('_C_6', 'C6'), ('_C_m7b5', 'Cm7b5'), ('_C_dim', 'Co'))), ('B', (('_B_', 'B'), ('_B_m', 'Bm'), ('_B_7', 'B7'), ('_B_m7', 'Bm7'), ('_B_maj7', 'BΔ'), ('_B_6', 'B6'), ('_B_m7b5', 'Bm7b5'), ('_B_dim', 'Bo'))), ('Bb', (('_Bb_', 'Bb'), ('_Bb_m', 'Bbm'), ('_Bb_7', 'Bb7'), ('_Bb_m7', 'Bbm7'), ('_Bb_maj7', 'BbΔ'), ('_Bb_6', 'Bb6'), ('_Bb_m7b5', 'Bbm7b5'), ('_Bb_dim', 'Bbo'))), ('A', (('_A_', 'A'), ('_A_m', 'Am'), ('_A_7', 'A7'), ('_A_m7', 'Am7'), ('_A_maj7', 'AΔ'), ('_A_6', 'A6'), ('_A_m7b5', 'Am7b5'), ('_A_dim', 'Ao'))), ('Ab', (('_Ab_', 'Ab'), ('_Ab_m', 'Abm'), ('_Ab_7', 'Ab7'), ('_Ab_m7', 'Abm7'), ('_Ab_maj7', 'AbΔ'), ('_Ab_6', 'Ab6'), ('_Ab_m7b5', 'Abm7b5'), ('_Ab_dim', 'Abo'))), ('G', (('_G_', 'G'), ('_G_m', 'Gm'), ('_G_7', 'G7'), ('_G_m7', 'Gm7'), ('_G_maj7', 'GΔ'), ('_G_6', 'G6'), ('_G_m7b5', 'Gm7b5'), ('_G_dim', 'Go'))), ('Gb', (('_Gb_', 'Gb'), ('_Gb_m', 'Gbm'), ('_Gb_7', 'Gb7'), ('_Gb_m7', 'Gbm7'), ('_Gb_maj7', 'GbΔ'), ('_Gb_6', 'Gb6'), ('_Gb_m7b5', 'Gbm7b5'), ('_Gb_dim', 'Gbo'))), ('F', (('_F_', 'F'), ('_F_m', 'Fm'), ('_F_7', 'F7'), ('_F_m7', 'Fm7'), ('_F_maj7', 'FΔ'), ('_F_6', 'F6'), ('_F_m7b5', 'Fm7b5'), ('_F_dim', 'Fo'))), ('E', (('_E_', 'E'), ('_E_m', 'Em'), ('_E_7', 'E7'), ('_E_m7', 'Em7'), ('_E_maj7', 'EΔ'), ('_E_6', 'E6'), ('_E_m7b5', 'Em7b5'), ('_E_dim', 'Eo'))), ('Eb', (('_Eb_', 'Eb'), ('_Eb_m', 'Ebm'), ('_Eb_7', 'Eb7'), ('_Eb_m7', 'Ebm7'), ('_Eb_maj7', 'EbΔ'), ('_Eb_6', 'Eb6'), ('_Eb_m7b5', 'Ebm7b5'), ('_Eb_dim', 'Ebo'))), ('D', (('_D_', 'D'), ('_D_m', 'Dm'), ('_D_7', 'D7'), ('_D_m7', 'Dm7'), ('_D_maj7', 'DΔ'), ('_D_6', 'D6'), ('_D_m7b5', 'Dm7b5'), ('_D_dim', 'Do'))), ('Db', (('_Db_', 'Db'), ('_Db_m', 'Dbm'), ('_Db_7', 'Db7'), ('_Db_m7', 'Dbm7'), ('_Db_maj7', 'DbΔ'), ('_Db_6', 'Db6'), ('_Db_m7b5', 'Dbm7b5'), ('_Db_dim', 'Dbo')))], default='-', max_length=10)),
                ('m4_b4', models.CharField(choices=[('.', '-'), ('C', (('_C_', 'C'), ('_C_m', 'Cm'), ('_C_7', 'C7'), ('_C_m7', 'Cm7'), ('_C_maj7', 'CΔ'), ('_C_6', 'C6'), ('_C_m7b5', 'Cm7b5'), ('_C_dim', 'Co'))), ('B', (('_B_', 'B'), ('_B_m', 'Bm'), ('_B_7', 'B7'), ('_B_m7', 'Bm7'), ('_B_maj7', 'BΔ'), ('_B_6', 'B6'), ('_B_m7b5', 'Bm7b5'), ('_B_dim', 'Bo'))), ('Bb', (('_Bb_', 'Bb'), ('_Bb_m', 'Bbm'), ('_Bb_7', 'Bb7'), ('_Bb_m7', 'Bbm7'), ('_Bb_maj7', 'BbΔ'), ('_Bb_6', 'Bb6'), ('_Bb_m7b5', 'Bbm7b5'), ('_Bb_dim', 'Bbo'))), ('A', (('_A_', 'A'), ('_A_m', 'Am'), ('_A_7', 'A7'), ('_A_m7', 'Am7'), ('_A_maj7', 'AΔ'), ('_A_6', 'A6'), ('_A_m7b5', 'Am7b5'), ('_A_dim', 'Ao'))), ('Ab', (('_Ab_', 'Ab'), ('_Ab_m', 'Abm'), ('_Ab_7', 'Ab7'), ('_Ab_m7', 'Abm7'), ('_Ab_maj7', 'AbΔ'), ('_Ab_6', 'Ab6'), ('_Ab_m7b5', 'Abm7b5'), ('_Ab_dim', 'Abo'))), ('G', (('_G_', 'G'), ('_G_m', 'Gm'), ('_G_7', 'G7'), ('_G_m7', 'Gm7'), ('_G_maj7', 'GΔ'), ('_G_6', 'G6'), ('_G_m7b5', 'Gm7b5'), ('_G_dim', 'Go'))), ('Gb', (('_Gb_', 'Gb'), ('_Gb_m', 'Gbm'), ('_Gb_7', 'Gb7'), ('_Gb_m7', 'Gbm7'), ('_Gb_maj7', 'GbΔ'), ('_Gb_6', 'Gb6'), ('_Gb_m7b5', 'Gbm7b5'), ('_Gb_dim', 'Gbo'))), ('F', (('_F_', 'F'), ('_F_m', 'Fm'), ('_F_7', 'F7'), ('_F_m7', 'Fm7'), ('_F_maj7', 'FΔ'), ('_F_6', 'F6'), ('_F_m7b5', 'Fm7b5'), ('_F_dim', 'Fo'))), ('E', (('_E_', 'E'), ('_E_m', 'Em'), ('_E_7', 'E7'), ('_E_m7', 'Em7'), ('_E_maj7', 'EΔ'), ('_E_6', 'E6'), ('_E_m7b5', 'Em7b5'), ('_E_dim', 'Eo'))), ('Eb', (('_Eb_', 'Eb'), ('_Eb_m', 'Ebm'), ('_Eb_7', 'Eb7'), ('_Eb_m7', 'Ebm7'), ('_Eb_maj7', 'EbΔ'), ('_Eb_6', 'Eb6'), ('_Eb_m7b5', 'Ebm7b5'), ('_Eb_dim', 'Ebo'))), ('D', (('_D_', 'D'), ('_D_m', 'Dm'), ('_D_7', 'D7'), ('_D_m7', 'Dm7'), ('_D_maj7', 'DΔ'), ('_D_6', 'D6'), ('_D_m7b5', 'Dm7b5'), ('_D_dim', 'Do'))), ('Db', (('_Db_', 'Db'), ('_Db_m', 'Dbm'), ('_Db_7', 'Db7'), ('_Db_m7', 'Dbm7'), ('_Db_maj7', 'DbΔ'), ('_Db_6', 'Db6'), ('_Db_m7b5', 'Dbm7b5'), ('_Db_dim', 'Dbo')))], default='-', max_length=10)),
                ('chord_seq', models.CharField(default='x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x', max_length=100)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('favorite', models.ManyToManyField(blank=True, related_name='favorite', to=settings.AUTH_USER_MODEL)),
                ('genre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='repo.Genre')),
                ('instrument', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='repo.Instrument')),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]
