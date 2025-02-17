import logging
import stripe
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from django.conf import settings
from .serializers import OrderSerializer
from .permissions import IsAdminUser  # Assure-toi que cette permission est bien définie dans permissions.py

logger = logging.getLogger(__name__)

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Convertir le panier en commande
        """
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"error": "Cart is empty"}, status=400)

        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        # Créer une commande
        order = Order.objects.create(user=request.user, total_price=0)
        total_price = 0

        for item in cart.items.all():
            if item.quantity > item.product.stock:
                return Response(
                    {"error": f"Not enough stock for {item.product.name}"},
                    status=400,
                )

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_per_unit=item.product.price,
            )

            item.product.stock -= item.quantity
            item.product.save()
            total_price += item.quantity * item.product.price

        order.total_price = total_price
        order.save()
        cart.items.all().delete()

        return Response({"message": "Order created successfully", "order_id": order.id}, status=201)


class UserOrdersView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class CreateStripePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            intent = stripe.PaymentIntent.create(
                amount=2000,
                currency="usd",
                metadata={"user_id": request.user.id},
            )
            return Response({"client_secret": intent['client_secret']})
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class StripeWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.headers.get('Stripe-Signature', '')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError:
            logger.error("Invalid payload")
            return Response({"error": "Invalid payload"}, status=400)
        except stripe.error.SignatureVerificationError:
            logger.error("Invalid signature")
            return Response({"error": "Invalid signature"}, status=400)

        if event['type'] == 'payment_intent.succeeded':
            logger.info("PaymentIntent succeeded event received.")
        elif event['type'] == 'charge.succeeded':
            logger.info("Charge succeeded event received.")
        else:
            logger.info(f"Unhandled event type: {event['type']}")

        return Response({"message": "Webhook received"}, status=200)


class AdminOrderActionsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, order_id):
        """
        Changer le statut d'une commande
        """
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()
        return Response({"message": f"Order {order_id} status updated to {new_status}."}, status=status.HTTP_200_OK)

    def delete(self, request, order_id):
        """
        Annuler une commande
        """
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if order.status in ['shipped', 'delivered']:
            return Response({"error": "Cannot cancel an order already shipped or delivered."},
                            status=status.HTTP_400_BAD_REQUEST)

        order.status = 'canceled'
        order.save()
        return Response({"message": f"Order {order_id} has been canceled."}, status=status.HTTP_200_OK)
