from django.urls import path
from . import views
from .views import (PostCreateView, PostDetailView, PostListView,
	PostUserView, PostUpdateView, PostDeleteView)
from data_loader import views as data_views


urlpatterns = [
	path('', views.home, name='start-page'),
	path('all_properties', PostListView.as_view(), name='all_info'),
	path('user/<str:username>/', PostUserView.as_view(), name='user-all-posts'),
	path('post/new/', PostCreateView.as_view(), name='user-create-post'),
	path('post/<int:pk>/', PostDetailView.as_view(), name='post-info'),
	path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
	path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
	path('property_analysis/', views.calculate_price , name='price-prediction'),
	path('property_analysis/<int:pk>/', views.calculate_price , name='price-prediction'),
	path('prediction_result/', views.present_result, name='prediction-result'),
	path('load_data/', data_views.inject_data, name='make_injection')
]
