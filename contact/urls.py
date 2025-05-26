from django.urls import path
from .views import submit_contact, respond_contact, list_contacts

urlpatterns = [
    # 📩 Soumission d’un message de contact par un utilisateur
    path('submit/', submit_contact, name='submit_contact'),

    # ✅ Traitement / réponse d’un message (via admin)
    path('respond/<int:pk>/', respond_contact, name='respond_contact'),

    # 📜 Liste complète des messages reçus (admin)
    path('messages/', list_contacts, name='list_contacts'),
]
