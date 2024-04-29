from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    genre = models.ForeignKey('self', on_delete=models.PROTECT, related_name='genres', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='images/books/')
    summary = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    genres = models.ManyToManyField(Genre)
    file = models.FileField(upload_to='books/', blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    verified = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at']


class BookFile(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='files')
    file_type = models.CharField(max_length=10)  # Например, 'pdf', 'epub'
    file = models.FileField(upload_to='books/')

    def __str__(self):
        return f"{self.book.title} ({self.file_type})"

    class Meta:
        verbose_name = 'Файл Книги'
        verbose_name_plural = 'Файлы Книг'


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    page = models.IntegerField(blank=True, default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - page {self.page}"

    class Meta:
        verbose_name = 'Марка Книги у пользователя'
        verbose_name_plural = 'Марки Книг у пользователей'


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Комментарий')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.book.title}'
