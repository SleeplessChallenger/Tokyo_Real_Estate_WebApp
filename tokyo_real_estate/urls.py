"""tokyo_real_estate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from prediction_price import views as predict_views
from data_loader import views as data_views
from users import views as user_views
from general import views as general_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('general.urls')),
    path('all-special-users/', user_views.display_users, name='show-all-users'),
    path('register/', user_views.register, name='register-newcomer'),
    path('login/', auth_views.LoginView.as_view(template_name=
            'users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name=
            'users/logout.html'), name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name=
            'users/password_reset.html'), name='reset-password'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name=
            'users/password_reset_done.html'), name='reset-password-done'),

    path('password-reset/confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='reset-password-confirm'),

    path('password-reset-finish/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_finish.html'), name='password-reset-finish'),

    path('delete-account/', user_views.delete_user, name='erase-user'),

    path('profile-info/', user_views.tweak_profile , name='profile'),

    path('property_analysis/', predict_views.calculate_price , name='price-prediction'),
    path('property_analysis/<int:pk>/', predict_views.calculate_price , name='price-prediction'),
    path('prediction_result/', predict_views.present_result, name='prediction-result'),

    path('load_data/', data_views.inject_data, name='make_injection'),

    path('api/', include('api.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
