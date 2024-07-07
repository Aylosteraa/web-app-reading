from django.urls import path
from . import views


urlpatterns = [
    path('<bookid>', views.forum, name='forum'),
    path('<bookid>/post', views.forumpost, name='forumpost'),
]