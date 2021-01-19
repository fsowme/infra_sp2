from api_yamdb.settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .custom_viewsets import ListCreateDestroyViewSet
from .filters import TitleFilter
from .models import (
    ADMIN,
    MODERATOR,
    USER,
    Category,
    Genre,
    Review,
    Title,
    User,
)
from .permissions import (
    IsAdminOrReadOnly,
    IsOwnerOrReadOnly,
    IsStaffOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleSerializerCreate,
    UserCodeSerializer,
    UserJwtSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["username"]
    lookup_field = "username"

    @action(
        methods=["PATCH"],
        detail=True,
        permission_classes=[permissions.IsAdminUser],
    )
    def perform_update(self, serializer):
        role = serializer.validated_data.get("role", None)
        if role is not None:
            if role == ADMIN:
                serializer.save(is_staff=True, is_superuser=True)
            if role == MODERATOR:
                serializer.save(is_staff=True, is_superuser=False)
            if role == USER:
                serializer.save(is_staff=False, is_superuser=False)
        else:
            serializer.save()

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        name="me",
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)


@api_view(["POST"])
def registration(request):
    email = request.data.get("email")
    user = get_object_or_404(User, email=email)
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()
    serializer = UserCodeSerializer(instance=user, data=request.data)
    if serializer.is_valid(raise_exception=True):
        mail_subject = "Код подтверждения"
        message = f"Ваш код подтверждения: {confirmation_code}"
        send_mail(
            mail_subject,
            message,
            DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            auth_user="user_email",
            auth_password="user_passowrd",
        )
    return Response(
        {"registration": f"Код подтверждения отправлен на почту: {email}"},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def get_jwt_token(request):
    serializer = UserJwtSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.data.get("email")
        confirmation_code = serializer.data.get("confirmation_code")
        user = get_object_or_404(User, email=email)
        if user.confirmation_code == confirmation_code:
            token = AccessToken.for_user(user)
            return Response({"token": f"{token}"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenresViewSet(ListCreateDestroyViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    lookup_field = "slug"


class CategoriesViewSet(ListCreateDestroyViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    lookup_field = "slug"


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    queryset = Title.objects.annotate(rating=Avg("reviews__score"))

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TitleSerializer
        return TitleSerializerCreate


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsOwnerOrReadOnly | IsStaffOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs["title_id"])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs["title_id"])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsOwnerOrReadOnly | IsStaffOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            title__id=self.kwargs["title_id"],
            id=self.kwargs["review_id"],
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs["review_id"])
        serializer.save(author=self.request.user, review=review)
