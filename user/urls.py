from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name=''),
	path('sign_in/', views.sign_in, name='sign_in'),
	path('sign_up/', views.sign_up, name='sign_up'),
	path('sign_up/sign_up_post/', views.sign_up_post, name='sign_up_post'),
	path('sign_in/sign_in_post/', views.sign_in_post, name='sign_in_post'),
	path('logout/', views.logout_view, name='logout_view'),
	path('user_update/', views.user_update, name='user_update'),
	path('user_update/update', views.update, name='update'),
    path('create/book', views.create_book, name='create_book'),
    path('create/book/userview/<bookid>', views.create_chapter, name='create_chapter'),
    path('create/book/chapter', views.createbook, name='createbook'),
	path('delete_planned/', views.delete_planned_book, name='delete_planned_book'),
]