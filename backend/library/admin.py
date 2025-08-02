from django.contrib import admin
from library.models import LibraryMember, Genre, Author, Language, Book, BookInstance, BookInstanceBorrowerRecord, Publisher

admin.site.register(LibraryMember)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Language)
admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(BookInstanceBorrowerRecord)
admin.site.register(Publisher)
