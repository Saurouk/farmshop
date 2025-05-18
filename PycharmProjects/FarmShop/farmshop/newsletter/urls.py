from django.urls import path
from .views import (
    subscribe,
    unsubscribe,
    newsletter_history,
    unsubscribe_confirm,
    send_newsletter,
)

urlpatterns = [
    path('subscribe/', subscribe, name='newsletter_subscribe'),
    path('unsubscribe/', unsubscribe, name='newsletter_unsubscribe'),
    path('unsubscribe/<str:token>/', unsubscribe_confirm, name='newsletter_unsubscribe_confirm'),
    path('history/', newsletter_history, name='newsletter_history'),
    path('send/', send_newsletter, name='newsletter_send'),
]
