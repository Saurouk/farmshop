from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import NewsletterSubscriber
from .serializers import NewsletterSubscriberSerializer

@api_view(['POST'])
def subscribe(request):
    serializer = NewsletterSubscriberSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
        if not created and not subscriber.is_active:
            subscriber.is_active = True
            subscriber.save()
        return Response({'message': "Inscription réussie à la newsletter."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
