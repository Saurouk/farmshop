from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings

@api_view(['POST'])
def submit_contact(request):
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        message = serializer.save()
        return Response({'message': 'Votre message a été envoyé.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_contacts(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    serializer = ContactMessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
def respond_contact(request, pk):
    try:
        message = ContactMessage.objects.get(pk=pk)
    except ContactMessage.DoesNotExist:
        return Response({'error': 'Message non trouvé.'}, status=status.HTTP_404_NOT_FOUND)

    response = request.data.get('response')
    if not response:
        return Response({'error': 'Une réponse est requise.'}, status=status.HTTP_400_BAD_REQUEST)

    message.response = response
    message.is_handled = True
    message.responded_at = now()
    message.save()

    send_mail(
        subject=f"Réponse à votre demande : {message.subject}",
        message=response,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[message.email],
        fail_silently=False,
    )

    return Response({'message': 'Réponse envoyée avec succès.'})
