from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoriesViewSet,
    CommentViewSet,
    GenresViewSet,
    ReviewViewSet,
    TitlesViewSet,
    UserViewSet,
    get_jwt_token,
    registration,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"genres", GenresViewSet, basename="genres")
router.register(r"categories", CategoriesViewSet, basename="categories")
router.register(r"titles", TitlesViewSet, basename="titles")
router.register(
    r"titles/(?P<title_id>[0-9]+)/reviews",
    ReviewViewSet,
    basename="review_by_post",
)
router.register(
    r"titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments",
    CommentViewSet,
    basename="comments_by_review",
)

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/auth/email/", registration, name="registration"),
    path("v1/auth/token/", get_jwt_token, name="token"),
]
