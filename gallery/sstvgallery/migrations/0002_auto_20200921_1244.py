# Generated by Django 3.0.8 on 2020-09-21 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sstvgallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='photo',
            field=models.ImageField(upload_to='received_images', verbose_name='SSTV Image'),
        ),
    ]