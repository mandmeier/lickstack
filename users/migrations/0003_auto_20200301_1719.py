# Generated by Django 3.0.2 on 2020-03-01 17:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repo', '0013_lick_favorite'),
        ('users', '0002_profile_liked_licks'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='faved_licks',
            field=models.ManyToManyField(blank=True, related_name='faved_licks', to='repo.Lick'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
