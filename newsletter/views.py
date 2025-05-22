from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import NewsletterSubscriber, Newsletter
from .serializers import NewsletterSubscriberSerializer, NewsletterSerializer
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def subscribe(request):
    email = request.data.get('email')
    logger.info(f"🟡 Tentative d'inscription avec : {email}")
    if not email:
        return Response({'error': 'Email requis.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save()
        elif subscriber.is_active:
            return Response({'error': 'Déjà inscrit à la newsletter.'}, status=status.HTTP_400_BAD_REQUEST)

        current_site = get_current_site(request)
        unsubscribe_url = f"http://{current_site.domain}/api/newsletter/unsubscribe/{subscriber.unsubscribe_token}/"

        subject = "Bienvenue à la newsletter FarmShop"
        body = "Merci pour votre inscription !"

        html_content = render_to_string('emails/newsletter.html', {
            'subject': subject,
            'body': body,
            'unsubscribe_url': unsubscribe_url,
        })

        msg = EmailMultiAlternatives(
            subject=subject,
            body=body,
            from_email=None,
            to=[email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        logger.info(f"✅ Email envoyé à : {email}")
        return Response({'message': "Inscription réussie à la newsletter."}, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"❌ Erreur pendant l'inscription : {str(e)}")
        return Response({'error': "Erreur serveur."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def unsubscribe(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email requis.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        subscriber = NewsletterSubscriber.objects.get(email=email)
        subscriber.is_active = False
        subscriber.save()
        return Response({'message': 'Désinscription réussie.'})
    except NewsletterSubscriber.DoesNotExist:
        return Response({'error': 'Adresse non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def unsubscribe_confirm(request, token):
    try:
        subscriber = NewsletterSubscriber.objects.get(unsubscribe_token=token)
        subscriber.is_active = False
        subscriber.save()
        return Response({'message': 'Vous avez été désabonné avec succès.'})
    except NewsletterSubscriber.DoesNotExist:
        return Response({'error': 'Lien invalide ou expiré.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def newsletter_history(request):
    newsletters = Newsletter.objects.all().order_by('-created_at')
    serializer = NewsletterSerializer(newsletters, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def send_newsletter(request):
    subject = request.data.get('subject')
    content = request.data.get('content')

    if not subject or not content:
        return Response({'error': 'Sujet et contenu requis.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        subscribers = NewsletterSubscriber.objects.filter(is_active=True)
        for subscriber in subscribers:
            unsubscribe_url = f"http://{get_current_site(request).domain}/api/newsletter/unsubscribe/{subscriber.unsubscribe_token}/"
            html_content = render_to_string('emails/newsletter.html', {
                'subject': subject,
                'body': content,
                'unsubscribe_url': unsubscribe_url,
            })
            msg = EmailMultiAlternatives(
                subject=subject,
                body=content,
                from_email=None,
                to=[subscriber.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        return Response({'message': 'Newsletter envoyée avec succès.'}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"❌ Erreur envoi newsletter : {str(e)}")
        return Response({'error': 'Erreur interne du serveur.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
