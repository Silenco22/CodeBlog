from unicodedata import name
from django.urls import path

from blog.views import (
    create_blog_view,
    detail_blog_view,
    edit_blog_view,
    edit_commnet_view,
    delete_commnet_view,
    add_like,
    add_dislike,
)

app_name = 'blog'

urlpatterns = [
    path('create/', create_blog_view, name="create"),
    path('<slug>/', detail_blog_view, name="detail"),
    path('<slug>/edit', edit_blog_view, name="edit"),
    # fix path
    path('<slug>/<int:pk>/comment/edit', edit_commnet_view, name="comment-edit"),
    path('<slug>/comment/<int:pk>/delete', delete_commnet_view, name="comment-delete"),
    path('<slug>/<int:pk>/like', add_like, name="like"),
    path('<slug>/<int:pk>/dislike', add_dislike, name="dislike"),
]
