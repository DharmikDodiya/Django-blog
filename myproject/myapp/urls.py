from django.urls import path
from . import views
from .views import CustomLoginView
# from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.upload_file, name='home'),
    path('upload_file', views.upload_file, name='upload_file'),
    # path('login_user/', views.login_user, name='login_user'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('register/', views.register_user, name='register_user'),
]