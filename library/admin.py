from django.contrib import admin
from .models import Genre, Tag, Book, BookFile, Bookmark


admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(Book)
admin.site.register(BookFile)
admin.site.register(Bookmark)
