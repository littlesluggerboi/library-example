from rest_framework import serializers
from library.models import Author, Book, Genre, Language, LibraryMember, BookInstance, BookInstanceBorrowerRecord, Publisher
from django.utils import timezone


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'date_of_birth',
            'date_of_death'
        ]

    def validate(self, data):
        dob = data.get('date_of_birth', None)
        dod = data.get('date_of_death', None)
        if (dob and dob > timezone.now().date()):
            raise serializers.ValidationError(
                "date_of_birth must be less than or equals to today.")

        if (dod and dod > timezone.now().date()):
            raise serializers.ValidationError(
                "date_of_death must be less than or equals to today.")
        if (dob and dod and dod < dob):
            raise serializers.ValidationError(
                "date_of_birth must be before date_of_death")
        return super().validate(data)


class AuthorDetailSerializer(serializers.ModelSerializer):
    class BookSerializer(serializers.ModelSerializer):
        class Meta:
            model = Book
            fields = ['title', 'isbn', 'publication_date']
    books = BookSerializer(many=True)

    class Meta:
        model = Author
        fields = [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'date_of_birth',
            'date_of_death',
            'books'
        ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = [
            'id',
            'name',
            'location'
        ]


class LibraryMembersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = LibraryMember
        fields = ['username', 'first_name', 'last_name', 'email', 'password']


class LibraryMemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryMember
        fields = ['username', 'password', 'first_name', 'last_name', 'email']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


class ActivateAccountSerializer(serializers.Serializer):
    username = serializers.CharField()


class BookSerializer(serializers.ModelSerializer):
    class GenreRepresentation(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = ['name']

    class PublisherRepresentation(serializers.ModelSerializer):
        class Meta:
            model = Publisher
            fields = ['name']

    class LanguageRepresentation(serializers.ModelSerializer):
        class Meta:
            model = Language
            fields = ['name']

    class AuthorRepresentation(serializers.ModelSerializer):
        class Meta:
            model = Author
            fields = ['first_name', 'last_name', 'middle_name']
    genre = GenreRepresentation(many=True)
    authors = AuthorRepresentation(many=True)
    publisher = PublisherRepresentation()
    language = LanguageRepresentation()

    class Meta:
        model = Book
        fields = ['title', 'summary', 'isbn', 'language',
                  'authors', 'genre', 'publisher', 'publication_date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        genres = []
        for genre in representation['genre']:
            genres.append(genre['name'])
        authors = []
        for author in representation['authors']:
            str = f'{author['last_name']}, {author['first_name']}'
            if author['middle_name']:
                str += f' {author['middle_name'][0]}.'
            authors.append(str)
        representation['genre'] = genres
        representation['authors'] = authors
        representation['language'] = representation['language']['name']
        if representation['publisher']:
            representation['publisher'] = representation['publisher']['name']
        return representation


class BookDetailSerializer(BookSerializer):
    class BookInstanceRepresentaion(serializers.ModelSerializer):
        class Meta:
            model = BookInstance
            fields = ['book_number', 'status']
    copies = BookInstanceRepresentaion(many=True)

    class Meta:
        model = Book
        fields = ['title', 'summary', 'isbn', 'language',
                  'authors', 'genre', 'publisher', 'publication_date', 'copies']


class BookUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    summary = serializers.CharField()
    isbn = serializers.CharField(max_length=13)
    language = serializers.IntegerField(min_value=1)
    publication_date = serializers.DateField(required=False, default=None)
    publisher = serializers.IntegerField(
        required=False, min_value=1, default=None)
    authors = serializers.ListField(
        child=serializers.IntegerField(min_value=1)
    )
    genre = serializers.ListField(
        child=serializers.IntegerField(min_value=1)
    )

    def validate_publication_date(self, value):
        if value and value > timezone.now().date():
            raise serializers.ValidationError(
                "Publication date must be set in the past")
        return value


class BookCreateSerialzier(BookUpdateSerializer):
    copies = serializers.IntegerField(min_value=0)


class BookPartialUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    summary = serializers.CharField(required=False)
    isbn = serializers.CharField(max_length=13, required=False)
    language = serializers.IntegerField(min_value=1, required=False)
    publication_date = serializers.DateField(required=False)
    publisher = serializers.IntegerField(
        required=False, min_value=1)
    authors = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=False
    )
    genre = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=False
    )

    def validate_publication_date(self, value):
        if value and value > timezone.now().date():
            raise serializers.ValidationError(
                "Publication date must be set in the past")
        return value


class BookInstanceSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = BookInstance
        fields = ['book_number', 'status', 'book']


class BookInstanceDetailSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class BorrowerSerializer(serializers.ModelSerializer):
        class Meta:
            model = LibraryMember
            fields = ['username']
    borrower = BorrowerSerializer()

    class Meta:
        model = BookInstance
        fields = ('book', 'book_number', 'status',
                  'date_borrowed', 'due_back', 'borrower')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if rep['borrower']:
            rep['borrower'] = rep['borrower']['username']
        return rep


class BookInstanceCreateSerializer(serializers.Serializer):
    book = serializers.IntegerField(min_value=1)


class BookInstanceBorrowSerializer(serializers.Serializer):
    return_date = serializers.DateField()

    def validate_return_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "return_date must be today onwards")
        if value > (timezone.now().date() + timezone.timedelta(weeks=2)):
            raise serializers.ValidationError(
                "Can borrow a book for a maximum of 2 weeks")
        return value


class BookRecordSerializer(serializers.ModelSerializer):
    borrower = LibraryMembersSerializer()

    class RecordSerializer(serializers.ModelSerializer):
        borrower = LibraryMembersSerializer()

        class Meta:
            model = BookInstanceBorrowerRecord
            fields = ['borrower', 'date_borrowed', 'due_back', 'date_returned']
    record = RecordSerializer(many=True)

    class Meta:
        model = BookInstance
        fields = ['borrower',
                  'date_borrowed', 'due_back', 'record']
