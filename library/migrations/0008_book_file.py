# Generated by Django 5.0.4 on 2024-04-28 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0007_book_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='books/'),
        ),
    ]