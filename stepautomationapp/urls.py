from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('', views.index, name='index'),
    path('account-profile', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('about/', views.aboutus, name='aboutus'),
    path('contacts-v3/', views.aboutus, name='contactus'),
    path('updateprofile', views.updateProfile, name='update-profile'),
    path('getcity', views.getCities),
    path('deleteaccount', views.delete_account, name='deleteaccount'),
    path('updateprofilepic', views.updateProfilePic, name='updateProfile'),
    path('steps', views.handleStepFiles, name='steps'),
    path('project/<projectName>', views.get_project_details)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
