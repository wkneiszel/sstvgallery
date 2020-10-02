# Generated by Django 3.0.8 on 2020-10-02 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sstvgallery', '0003_comment_commentor'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, verbose_name='Average Rating'),
        ),
        migrations.AddField(
            model_name='image',
            name='votes',
            field=models.IntegerField(default=0, verbose_name='Vote Count'),
        ),
    ]
