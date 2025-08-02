from rest_framework import viewsets, permissions, response, status
from rest_framework.decorators import action
from library import serializers, models
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from django.db.models import Max
# bookInstance
# - borrow a book - user
# - return a book - user
# - make a book unavailable - admin
# - get list of bookinstance - admin and user
# - get detail of bookinstance - admin and user **additional detail for admin
# - disable a bookinstance - admin
# - filtering shit for the list field
# - create a bookinstance - admin
# - update is disabled
# - patch is disabled
# - delete is possible i guess


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = models.Author.objects.all().order_by('first_name')
    serializer_class = serializers.AuthorSerializer

    def get_queryset(self):
        if (self.action == 'retrieve'):
            return models.Author.objects.prefetch_related('books').all().order_by('first_name')
        return super().get_queryset()

    def get_permissions(self):
        self.permission_classes = [permissions.IsAdminUser]
        if self.action == 'retrieve' or self.action == 'list':
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if (self.action == 'retrieve'):
            return serializers.AuthorDetailSerializer
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        serializer = serializers.AuthorSerializer(data=request.data)
        if (serializer.is_valid()):
            request_payload = serializer.data
            author = self.get_object()
            for field in request_payload.keys():
                setattr(author, field, request_payload.get(field, None))
            author.save()
            response_payload = self.get_serializer(author).data
            return response.Response(data=response_payload, status=status.HTTP_200_OK)
        return super().update(request, *args, **kwargs)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = models.Genre.objects.all().order_by('name')
    serializer_class = serializers.GenreSerializer

    def get_permissions(self):
        self.permission_classes = [permissions.IsAdminUser]
        if self.action == 'retrieve' or self.action == 'list':
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = models.Language.objects.all().order_by('name')
    serializer_class = serializers.LanguageSerializer

    def get_permissions(self):
        self.permission_classes = [permissions.IsAdminUser]
        if self.action == 'retrieve' or self.action == 'list':
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = models.Publisher.objects.all().order_by('name')
    serializer_class = serializers.PublisherSerializer

    def get_permissions(self):
        self.permission_classes = [permissions.IsAdminUser]
        if self.action == 'retrieve' or self.action == 'list':
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        serializer = serializers.PublisherSerializer(data=request.data)
        if (serializer.is_valid()):
            request_payload = serializer.data
            publisher = self.get_object()
            for field in request_payload.keys():
                setattr(publisher, field, request_payload.get(field, None))
                response_payload = self.get_serializer(publisher).data
            publisher.save()
            return response.Response(data=response_payload, status=status.HTTP_200_OK)
        return super().update(request, *args, **kwargs)


class LibraryMemberViewSet(viewsets.ModelViewSet):
    queryset = models.LibraryMember.objects.all().order_by('username')
    serializer_class = serializers.LibraryMembersSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_object(self):
        if self.action in ['member_profile', 'change_password']:
            return self.request.user
        return super().get_object()

    def get_permissions(self):
        if (self.action in ['member_profile', 'change_password', 'deactivate']):
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        if self.action == 'member_profile':
            return super().update(request, *args, **kwargs)
        return response.Response({'detail': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return response.Response({'detail': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['get', 'patch'], url_path='profile', url_name='profile')
    def member_profile(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            return self.partial_update(request=request)

    @action(detail=False, methods=['post'], url_name='change-password', url_path='change-password')
    def change_password(self, request):
        """Change password of logged in user"""
        serializer = serializers.ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = self.get_object()
        req_payload = serializer.data
        if (not member.check_password(req_payload['old_password'])):
            return response.Response(data={'detail': 'password does not match'}, status=status.HTTP_400_BAD_REQUEST)
        member.set_password(req_payload['new_password'])
        member.save()
        return response.Response(data={'Password changed'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_name='deactivate', url_path='deactivate')
    def deactivate(self, request, pk):
        member = self.get_object()
        if request.user.id == int(pk) or request.user.is_superuser:
            member.is_active = False
            member.save()
            return response.Response(data={'detail': 'Account deactivated.'}, status=status.HTTP_200_OK)
        return response.Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['post'], url_name='activate', url_path='activate')
    def activate(self, request):
        serializer = serializers.ActivateAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        req_payload = serializer.data
        member = get_object_or_404(
            self.get_queryset(), username=req_payload['username'])
        member.is_active = True
        member.save()
        return response.Response(data={'detail': f'Account with username: {req_payload['username']} activated.'}, status=status.HTTP_200_OK)


class BookViewSet(viewsets.ModelViewSet):
    queryset = models.Book.objects.prefetch_related('authors', 'genre').select_related(
        'publisher', 'language').all().order_by('title')
    serializer_class = serializers.BookSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.BookDetailSerializer
        if self.action == 'create':
            return serializers.BookCreateSerialzier
        if self.action == 'update':
            return serializers.BookUpdateSerializer
        if self.action == 'partial_update':
            return serializers.BookPartialUpdateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        req_payload = serializer.data
        try:
            with transaction.atomic():
                authors = req_payload.pop('authors')
                publisher = req_payload.pop('publisher', None)
                language = req_payload.pop('language')
                genres = req_payload.pop('genre')
                copies = req_payload.pop('copies')

                book = models.Book.objects.create(**req_payload)
                for author_id in authors:
                    author = models.Author.objects.get(pk=author_id)
                    book.authors.add(author)
                for genre_id in genres:
                    genre = models.Genre.objects.get(pk=genre_id)
                    book.genre.add(genre)
                book.language = models.Language.objects.get(pk=language)
                if publisher != None:
                    book.publisher = models.Publisher.objects.get(pk=publisher)
                book.save()
                for book_number in range(1, copies+1):
                    models.BookInstance.objects.create(
                        book_number=book_number, book=book)

                serializer = serializers.BookDetailSerializer(instance=book)
                return response.Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(data={'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        req_payload = serializer.data
        try:
            with transaction.atomic():
                book = self.get_object()
                language = req_payload.pop('language')
                publisher = req_payload.pop('publisher', None)
                authors = req_payload.pop('authors')
                genres = req_payload.pop('genre')

                book.language = models.Language.objects.get(pk=language)
                if publisher != None:
                    book.publisher = models.Publisher.objects.get(pk=publisher)
                else:
                    book.publisher = publisher
                book.authors.clear()
                for author_id in authors:
                    author = models.Author.objects.get(pk=author_id)
                    book.authors.add(author)
                book.genre.clear()
                for genre_id in genres:
                    genre = models.Genre.objects.get(pk=genre_id)
                    book.genre.add(genre)
                for field in req_payload.keys():
                    setattr(book, field, req_payload.get(field))
                book.save()
                deserializer = serializers.BookSerializer(instance=book)
                return response.Response(data=deserializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(data={'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        req_payload = serializer.data
        try:
            with transaction.atomic():
                book = self.get_object()
                language = req_payload.pop('language', None)
                publisher = req_payload.pop('publisher', None)
                authors = req_payload.pop('authors', None)
                genres = req_payload.pop('genre', None)

                if language != None:
                    book.language = models.Language.objects.get(pk=language)
                if publisher != None:
                    book.publisher = models.Publisher.objects.get(pk=publisher)
                if authors != None:
                    book.authors.clear()
                    for author_id in authors:
                        author = models.Author.objects.get(pk=author_id)
                        book.authors.add(author)
                if genres != None:
                    book.genre.clear()
                    for genre_id in genres:
                        genre = models.Genre.objects.get(pk=genre_id)
                        book.genre.add(genre)
                for field in req_payload.keys():
                    setattr(book, field, req_payload.get(field))
                book.save()
                deserializer = serializers.BookSerializer(instance=book)
                return response.Response(data=deserializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(data={'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return response.Response(data={'detail': 'Delete operation is not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class BookInstanceViewSet(viewsets.ModelViewSet):
    queryset = models.BookInstance.objects.select_related('book', 'borrower').prefetch_related(
        'record').all().order_by('book__title', 'book_number')
    serializer_class = serializers.BookInstanceSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action in ['retrieve', 'disable', 'return_book']:
            return serializers.BookInstanceDetailSerializer
        if self.action == 'create':
            return serializers.BookInstanceCreateSerializer
        if self.action == 'borrow':
            return serializers.BookInstanceBorrowSerializer
        if self.action == 'record':
            return serializers.BookRecordSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', 'disable', 'record']:
            self.permission_classes = [permissions.IsAdminUser]
        if self.action in ['borrow', 'return_book']:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        try:
            with transaction.atomic():
                book = models.Book.objects.get(pk=data.pop('book'))
                next_book_number = models.BookInstance.objects.filter(
                    book=book).aggregate(Max('book_number'))
                book_number = next_book_number.pop('book_number__max') or 0
                book_instance = models.BookInstance.objects.create(
                    book=book, book_number=(book_number+1))
                deserailizer = serializers.BookInstanceDetailSerializer(
                    instance=book_instance)
                return response.Response(data=deserailizer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return response.Response(data={'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        return response.Response(data={'detail': 'Method PUT is not allowed for this resource'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return response.Response(data={'detail': 'Method PATCH is not allowed for this resource'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return response.Response(data={'detail': 'Method DELETE is not allowed for this resource'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=['post'], url_name='borrow', url_path='borrow')
    def borrow(self, request, pk):
        # book_instance = models.BookInstance.objects.get()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        due_back = serializer.data['return_date']
        date_borrowed = timezone.now().date()
        try:
            with transaction.atomic():
                book_instance = self.get_object()
                if (book_instance.status != 'Available'):
                    raise Exception(
                        f'The book is currently {book_instance.status}')
                book_instance.date_borrowed = date_borrowed
                book_instance.due_back = due_back
                book_instance.borrower = request.user
                book_instance.status = "On Loan"
                book_instance.save()
                deserializer = serializers.BookInstanceDetailSerializer(
                    instance=book_instance)
                return response.Response(data=deserializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(data={'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_name='disable', url_path='disable')
    def disable(self, request, pk):
        book_instance = self.get_object()
        if book_instance.status == 'On Loan':
            return response.Response(data={'detail': f'Cannot disable. The book is currently on loan.'}, status=status.HTTP_400_BAD_REQUEST)
        book_instance.status = 'Unavailable'
        book_instance.save()
        serializer = self.get_serializer(instance=book_instance)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_name='return_book', url_path='return_book')
    def return_book(self, request, pk):
        book_instance = self.get_object()
        borrower = book_instance.borrower
        if not borrower:
            return response.Response(data={'detail': 'Book is not On Loan.'}, status=status.HTTP_400_BAD_REQUEST)
        if borrower.id != request.user.id:
            return response.Response(data={'detail': 'Cannot return a borrow you did not borrowe'}, status=status.HTTP_400_BAD_REQUEST)
        date_borrowed = book_instance.date_borrowed
        due_back = book_instance.due_back
        date_returned = timezone.now().date()
        try:
            with transaction.atomic():
                models.BookInstanceBorrowerRecord.objects.create(
                    book_instance=book_instance, borrower=borrower, date_borrowed=date_borrowed, due_back=due_back, date_returned=date_returned)
                book_instance.status = 'Available'
                book_instance.borrower = None
                book_instance.date_borrowed = None
                book_instance.due_back = None
                book_instance.save()
        except Exception as e:
            return response.Response(data={'detail': f'{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = self.get_serializer(instance=book_instance)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_name='record', url_path='record')
    def record(self, request, pk):
        book_instance = self.get_object()
        serializer = self.get_serializer(instance=book_instance)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)
