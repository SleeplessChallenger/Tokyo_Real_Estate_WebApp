from django.urls import path
from . import views
from .views import (PostCreateView, PostDetailView, PostListView,
	PostUserView, PostUpdateView, PostDeleteView, PostDeleteAll)


urlpatterns = [
	path('', views.home, name='start-page'),
	path('all_properties', PostListView.as_view(), name='all_info'),
	path('user/<str:username>/', PostUserView.as_view(), name='user-all-posts'),
	path('post/new/', PostCreateView.as_view(), name='user-create-post'),
	path('post/<int:pk>/', PostDetailView.as_view(), name='post-info'),
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
	path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
	path('post/<str:username>/delete_all/', PostDeleteAll.as_view(), name='erase-all-posts')
]
