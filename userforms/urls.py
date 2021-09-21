from django.urls import path
from . import views

urlpatterns = [
    path('', views.userforms, name='userforms'),
    path('getform', views.handleForm),
    path('publish/<int:form_id>', views.publishForm),
    path('responses/<int:id>',views.get_form_responses),
    path('processform', views.processForm),
    path('getforms', views.get_all_forms),
]
