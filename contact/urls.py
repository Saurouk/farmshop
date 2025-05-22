from django.urls import path
from .views import submit_contact, respond_contact, list_contacts

urlpatterns = [
    path('submit/', submit_contact, name='submit_contact'),
    path('respond/<int:pk>/', respond_contact, name='respond_contact'),
    path('messages/', list_contacts, name='list_contacts'),
]
