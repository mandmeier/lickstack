# Generated by Django 3.0.5 on 2020-08-26 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0006_auto_20200508_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='lick',
            name='notes',
            field=models.TextField(blank=True, default='', max_length=500, null=True),
        ),
    ]
