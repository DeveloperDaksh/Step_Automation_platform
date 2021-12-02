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
    path('project/<projectName>', views.get_project_details),
    path('forget-password', views.forgetPassword, name='forgetpassword'),
    path('update-password/<token>', views.update_password, name='update_password'),
    path('createsteps', views.create_steps, name='create_steps'),
    path('displaysteps', views.display_steps, name='display_steps'),
    path('dashboard', views.dashboard_details, name='dashboard_details'),
    path('templates', views.template_details, name='templates'),
    path('documents', views.documents_details, name='documents'),
    path('clients', views.clients_details, name='clients'),
    path('cases', views.cases_details, name='cases'),
    path('createdocument', views.create_document, name='create_document'),
    path('customers', views.customers_details, name='customer_details'),
    path('projects', views.project_details, name='project_details'),
    path('createcustomer', views.create_customer, name='create_customer'),
    path('editcustomer/<int:customer_id>', views.edit_customer),
    path('deletecustomer/<int:customer_id>', views.delete_customer)

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
