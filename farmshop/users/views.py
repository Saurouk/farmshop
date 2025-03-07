from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics, status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer, MessageSerializer, AdminDashboardSerializer
from .models import Message
from products.models import Product
from blog.models import Article, Comment

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """ Retourne les infos de l'utilisateur connecté avec sa boîte de réception """
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_users(request):
    """ ✅ Endpoint pour voir tous les utilisateurs (admin uniquement) """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, user_id):
    """ ✅ Endpoint pour supprimer un utilisateur (admin uniquement) """
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({"message": "Utilisateur supprimé avec succès."}, status=200)
    except User.DoesNotExist:
        return Response({"error": "Utilisateur non trouvé."}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard(request):
    """ ✅ Retourne les statistiques pour l'admin """
    if not request.user.is_staff:
        return Response({"error": "Accès refusé. Vous n'êtes pas admin."}, status=403)

    stats = {
        "total_users": User.objects.count(),
        "total_products": Product.objects.count(),
        "total_blog_posts": Article.objects.count(),
        "reported_comments": Comment.objects.filter(report__resolved=False).count(),
    }

    return Response(stats, status=200)


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
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API pour l'envoi et la réception des messages entre utilisateurs.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    ✅ Surcharge la connexion pour inclure les infos utilisateur
    """

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Identifiants manquants."}, status=400)

        user = authenticate(username=username, password=password)

        if user is not None:
            response.data["user"] = UserSerializer(user).data
        else:
            return Response({"error": "Nom d'utilisateur ou mot de passe incorrect."}, status=401)

        return response
