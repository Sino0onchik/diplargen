from django.urls import path
from django.contrib.auth.views import LoginView
from .views import HomeView, GenreBooksView, BookDetailView, BookmarkUpdateView, RegisterView, logout_acc, add_book

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(template_name='login.html', success_url='/'), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_acc, name='logout'),
    path('genre/<int:genre_id>/', GenreBooksView.as_view(), name='genre_books'),
    path('book/<int:pk>', BookDetailView.as_view(), name='book_detail'),
    path('books/<int:pk>/bookmark/', BookmarkUpdateView.as_view(), name='update_bookmark'),
    path('add_book/', add_book, name='add_book'),
]
