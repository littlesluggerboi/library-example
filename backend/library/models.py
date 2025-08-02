from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class LibraryMember(AbstractUser):
    class Meta:
        verbose_name = ("member")
        verbose_name_plural = ("members")


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            models.functions.Lower('name'),
            name='genre_name_case_insensitive_unique',
            violation_error_message='Genre already exists (case insensitive match).'
        )]

    def __str__(self):
        return f'{self.name}'


class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(date_of_birth__isnull=True) | models.Q(
                    date_of_birth__lte=timezone.now()),
                name='date_of_birth_lte_today'
            ),
            models.CheckConstraint(
                check=models.Q(date_of_death__isnull=True) | models.Q(
                    date_of_death__lte=timezone.now()),
                name='date_of_death_lte_today'
            ),
            models.CheckConstraint(
                check=(models.Q(date_of_death__gte=models.F('date_of_birth'))),
                name='date_of_death_gte_date_of_birth'
            )
        ]

    def __str__(self):
        return f'{self.last_name}, {self.first_name} {self.middle_name}'


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            models.functions.Lower('name'),
            name='language_name_case_insensitive_unique',
            violation_error_message='Language already exists (case insensitive match).'
        )]

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField()
    genre = models.ManyToManyField(Genre, related_name="books")
    authors = models.ManyToManyField(Author,  related_name="books")
    language = models.ForeignKey(
        Language, null=True, on_delete=models.SET_NULL)
    publication_date = models.DateField(null=True, blank=True)
    publisher = models.ForeignKey(
        Publisher, null=True, on_delete=models.RESTRICT)
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(publication_date__isnull=True) | models.Q(
                    publication_date__lte=timezone.now()),
                name='publication_date_cannot_be_after_today'
            )
        ]

    def __str__(self):
        return f"{self.title}"


class BookInstance(models.Model):
    book_number = models.PositiveIntegerField()
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, related_name='copies')
    date_borrowed = models.DateField(null=True)
    due_back = models.DateField(null=True)
    borrower = models.ForeignKey(to="LibraryMember", on_delete=models.RESTRICT, null=True)
    class StatusChoices(models.TextChoices):
        AVAILABLE = "Available"
        ON_LOAN = "On Loan"
        UNAVAILABLE = "Unavailable"

    status = models.CharField(
        max_length=50, choices=StatusChoices.choices, default=StatusChoices.AVAILABLE)

    class Meta:
        unique_together = (("book", "book_number"))
        constraints = [
            models.CheckConstraint(
                check=(models.Q(date_borrowed__isnull=True) | models.Q(
                    date_borrowed__gte=timezone.now())),
                name='date_borrowed_null_or_gte_today'
            ),
            models.CheckConstraint(
                check=(models.Q(due_back__isnull=True) & models.Q(date_borrowed__isnull=True)) |
                (models.Q(date_borrowed__isnull=False) & models.Q(due_back__isnull=False) &
                 models.Q(due_back__gte=models.F('date_borrowed'))),
                name='both_null_or_present_and_due_back_gte_due_back'
            ),
        ]
    


class BookInstanceBorrowerRecord(models.Model):
    book_instance = models.ForeignKey(BookInstance, on_delete=models.RESTRICT, related_name='record')
    borrower = models.ForeignKey(LibraryMember, on_delete=models.RESTRICT)
    date_borrowed = models.DateField()
    due_back = models.DateField()
    date_returned = models.DateField()

    def __str__(self):
        return f"Borrower's Card: {self.borrower.username} borrowed by {self.book_instance.book.title} on {self.date_borrowed}"
