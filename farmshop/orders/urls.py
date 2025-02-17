from django.urls import path
from .views import CreateOrderView, UserOrdersView, CreateStripePaymentIntentView, StripeWebhookView, \
    AdminOrderActionsView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('history/', UserOrdersView.as_view(), name='order-history'),
    path('admin/<int:order_id>/update-status/', AdminOrderActionsView.as_view(), name='update-order-status'),
    path('admin/<int:order_id>/cancel/', AdminOrderActionsView.as_view(), name='cancel-order'),
    path('create-payment-intent/', CreateStripePaymentIntentView.as_view(), name='create-payment-intent'),
    path('stripe-webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),  # Webhook
]
