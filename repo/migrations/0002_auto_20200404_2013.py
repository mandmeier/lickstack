# Generated by Django 3.0.2 on 2020-04-04 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instrument',
            options={'ordering': ('name',)},
        ),
        migrations.RemoveField(
            model_name='lick',
            name='m1_b1',
        ),
        migrations.RemoveField(
            model_name='lick',
            name='m1_b2',
        ),
        migrations.RemoveField(
            model_name='lick',
            name='m1_b3',
        ),
        migrations.RemoveField(
            model_name='lick',
            name='m1_b4',
        ),
        migrations.RemoveField(
            model_name='lick',
            name='m2_b1',
        ),
        migrations.RemoveField(
            model_name='lick',
            name='m2_b2',
        ),
        migrations.RemoveField(
            model_name='lick',
            name='m2_b3',
        ),
        migrations.RemoveField(
            model_name='lick',
            name='m2_b4',
        ),
        migrations.RemoveField(
            model_name='lick',
            name='m3_b1',
        ),
        migrations.RemoveField(
            model_name='lick',
            name='m3_b2',
        ),
        migrations.RemoveField(
            model_name='lick',
            name='m3_b3',
        ),
        migrations.RemoveField(
            model_name='lick',
            name='m3_b4',
        ),
        migrations.RemoveField(
            model_name='lick',
            name='m4_b1',
        ),
        migrations.RemoveField(
            model_name='lick',
            name='m4_b2',
        ),
        migrations.RemoveField(
            model_name='lick',
            name='m4_b3',
        ),
        migrations.RemoveField(
            model_name='lick',
            name='m4_b4',
        ),
        migrations.AddField(
            model_name='lick',
            name='transpose_rule',
            field=models.CharField(default='b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b', max_length=100),
        ),
    ]
