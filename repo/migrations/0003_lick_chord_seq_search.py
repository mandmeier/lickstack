# Generated by Django 3.0.2 on 2020-04-04 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0002_auto_20200404_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='lick',
            name='chord_seq_search',
            field=models.CharField(default='x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x.x', max_length=100),
        ),
    ]
