from . import views
from django.urls import include, path
from rest_framework import routers
from django.contrib.auth.models import User


router = routers.DefaultRouter()
router.register(r'profile', views.ProfileViewSet)



urlpatterns = [
	path('', include(router.urls)),
	path('users/', views.UserView.as_view(), name='all-users-api'),
	path('user/<int:pk>', views.UserView.as_view(), name='one-user-api'),
	path('properties/', views.PropertyView.as_view(), name='all-properties-api'),
	path('properties/<int:pk>', views.PropertyView.as_view(), name='one-property-api'),

]
