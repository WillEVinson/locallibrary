from django.contrib import admin

# Register your models here.
from .models import Author, Genre, Book, BookInstance, Language, BookAuthor

# consider adding save_as to more easily add instance that have similar values
# you could do this for any or all of the below, e.g.
# admin.site.register(Book, save_as=True)
# except mayeb not bookinstance tho

admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(BookAuthor)


class BookAuthorInline(admin.TabularInline):
    model = BookAuthor
    extra = 1

# Define the admin class
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    inlines = [BookAuthorInline]
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_authors', 'display_genre')
    inlines = [BookAuthorInline, BooksInstanceInline]
    @admin.display(description='Authors')
    def display_authors(self, obj):
        """Comma-separated authors in order (a ManyToManyField can't go directly in list_display)."""
        return ', '.join(str(ba.author) for ba in obj.bookauthor_set.select_related('author'))

# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

