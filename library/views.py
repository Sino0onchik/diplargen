from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import Q
from django.views.generic import FormView

from .forms import UserRegistrationForm, CommentForm, BookForm
from .models import Book, Genre, Bookmark
from django.contrib.auth import get_user_model, login, authenticate, logout

User = get_user_model()


class HomeView(generic.ListView):
    model = Book
    queryset = Book.objects.filter(verified=True, is_active=True)
    template_name = 'index.html'
    context_object_name = 'books'
    paginate_by = 20  # Количество книг на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        sort = self.request.GET.get('sort', 'title')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query)
            )

        if sort == 'date':
            queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by(sort)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()  # Добавляем жанры в контекст
        return context


class GenreBooksView(generic.ListView):
    model = Book
    template_name = 'genre_detail.html'
    context_object_name = 'books'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        genre_id = self.kwargs.get('genre_id')
        query = self.request.GET.get('q')
        sort = self.request.GET.get('sort', 'title')

        if genre_id:
            queryset = queryset.filter(genres__id=genre_id)

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query)
            )

        if sort == 'date':
            queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre'] = Genre.objects.get(id=self.kwargs.get('genre_id'))
        return context


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = 'book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            # Проверка, есть ли закладка на эту книгу для пользователя
            bookmark, created = Bookmark.objects.get_or_create(user=user, book=self.object)
            context['bookmark'] = bookmark
            context['comment_form'] = CommentForm()
        else:
            return context
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.book = self.get_object()
            comment.author = request.user
            comment.save()
            return redirect('book_detail', pk=comment.book.pk)
        return self.get(request, *args, **kwargs)


class BookmarkUpdateView(generic.View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        page = request.POST.get('page')
        if request.user.is_authenticated:
            bookmark, created = Bookmark.objects.get_or_create(user=request.user, book=book)
            bookmark.page = page
            bookmark.save()
        return redirect('book_detail', pk=pk)


class RegisterView(FormView):
    form_class = UserRegistrationForm
    template_name = 'auth/register.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.auth_provider = False
        form.save()

        authenticated_user = authenticate(email=user.email, password=form.cleaned_data['password1'])
        if authenticated_user is not None:
            login(self.request, authenticated_user)

        return super().form_valid(form)


@login_required(login_url='login')
def logout_acc(request):
    logout(request)
    return redirect('/')


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect('/')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})