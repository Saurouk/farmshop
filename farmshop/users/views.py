from django.contrib.auth import get_user_model
from rest_framework import generics, status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, MessageSerializer
from .models import Message

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """ Retourne les infos de l'utilisateur connecté """
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

class RegisterView(generics.CreateAPIView):
    """
    API pour l'inscription d'un nouvel utilisateur.
    Retourne également les tokens JWT à la création du compte.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    """
    API pour la gestion des utilisateurs.
    - Un admin peut voir tous les utilisateurs.
    - Un utilisateur normal peut voir/modifier son propre profil.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # ✅ Un admin voit tous les utilisateurs
            return User.objects.all()
        return User.objects.filter(id=user.id)  # ✅ Un utilisateur normal ne voit que son propre profil

class MessageViewSet(viewsets.ModelViewSet):
    """
    API pour l'envoi et la réception des messages entre utilisateurs.
    - Un utilisateur ne peut voir que ses propres messages reçus.
    - Un admin peut voir tous les messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # ✅ Un admin voit tous les messages
            return Message.objects.all()
        return Message.objects.filter(recipient=user)  # ✅ Un utilisateur normal ne voit que ses messages reçus

    def perform_create(self, serializer):
        """
        Lorsqu'un message est envoyé, l'expéditeur est automatiquement défini comme l'utilisateur connecté.
        """
        serializer.save(sender=self.request.user)


