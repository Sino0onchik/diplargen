# Generated by Django 5.0.4 on 2024-04-27 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_alter_genre_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(default=1, upload_to='images/books/'),
            preserve_default=False,
        ),
    ]
