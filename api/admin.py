from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        "name",
        "slug",
    )
    search_fields = ("name",)


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        "name",
        "slug",
    )
    search_fields = ("name",)


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "description",
        "category",
        "genre_for_admin",
    )
    search_fields = (
        "name",
        "year",
    )
    empty_value_display = "(None)"


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "pub_date", "title", "score")
    search_fields = ("pub_date", "title")
    empty_value_display = "(None)"


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "bio", "email")
    search_fields = ("first_name",)
    empty_value_display = "(None)"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "pub_date", "review")
    search_fields = ("author", "review")
    empty_value_display = "(None)"


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
