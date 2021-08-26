from django.urls import path
from . import views

urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('', views.index, name='index'),
    path('<token>/account-profile', views.dashboard, name='dashboard'),
    path('<token>/logout', views.logout, name='logout'),
    path('about/', views.aboutus, name='aboutus'),
    path('contacts-v3/', views.aboutus, name='contactus'),
]
