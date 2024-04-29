from django import forms

from .models import Comment, Book


class UserRegistrationForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['username', 'password']


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'border p-2 rounded w-full'}), label='Комментарий')

    class Meta:
        model = Comment
        fields = ('text',)


class BookForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}))
    author = forms.CharField(widget=forms.TextInput(attrs={'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}))
    summary = forms.CharField(widget=forms.Textarea(attrs={'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}))
    cover_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}))
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'}))

    class Meta:
        model = Book
        fields = ['title', 'author', 'summary', 'cover_image', 'file', 'genres']
