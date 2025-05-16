from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from django.shortcuts import redirect
from rest_framework import generics, status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes, action, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer, MessageSerializer, AdminDashboardSerializer
from .models import Message
from products.models import Product, Rental
from blog.models import Article, Comment
from orders.models import Order

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from django.http import FileResponse
from django.conf import settings
import zipfile
import os
import tempfile
import json

User = get_user_model()


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def get_current_user(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    if request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    user.delete()
    return Response({"message": "Votre compte a été supprimé avec succès."})


@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({"message": "Utilisateur supprimé avec succès."})
    except User.DoesNotExist:
        return Response({"error": "Utilisateur non trouvé."}, status=404)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "Utilisateur non trouvé."}, status=404)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        return Response(UserSerializer(user).data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_dashboard(request):
    stats = {
        "total_users": User.objects.count(),
        "total_products": Product.objects.count(),
        "total_blog_posts": Article.objects.count(),
        "reported_comments": Comment.objects.filter(report__resolved=False).count(),
    }
    return Response(stats)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            activation_link = f"http://{current_site.domain}/api/users/confirm/{uid}/{token}/"

            subject = "Activation de votre compte FarmShop"
            message = f"Bonjour {user.username},\n\nMerci de vous être inscrit sur FarmShop !\n\nVeuillez cliquer sur le lien ci-dessous pour activer votre compte :\n\n{activation_link}\n\nSi vous n'avez pas demandé cette inscription, ignorez ce message."

            send_mail(subject, message, None, [user.email], fail_silently=False)
            return Response({"message": "Inscription réussie. Vérifiez votre boîte mail."}, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([AllowAny])
def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, OverflowError):
        return redirect('http://localhost:5173/activation-failed')

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('http://localhost:5173/activation-success')
    else:
        return redirect('http://localhost:5173/activation-failed')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [JSONParser]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        recipient_username = self.request.data.get('recipient')
        try:
            recipient_user = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Destinataire introuvable.")
        serializer.save(sender=self.request.user, recipient=recipient_user)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Identifiants manquants."}, status=400)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"error": "Nom d'utilisateur ou mot de passe incorrect."}, status=401)

        if not user.is_active:
            return Response({"error": "Votre compte n'est pas activé."}, status=403)

        update_last_login(None, user)
        response = super().post(request, *args, **kwargs)
        response.data["user"] = UserSerializer(user).data
        return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_user_data(request):
    user = request.user
    temp_dir = tempfile.mkdtemp()

    user_data = {
        "username": user.username,
        "email": user.email,
        "bio": user.bio,
    }

    with open(os.path.join(temp_dir, "user.json"), "w") as f:
        json.dump(user_data, f)

    def write_json(name, queryset):
        with open(os.path.join(temp_dir, f"{name}.json"), "w") as f:
            json.dump([
                {field.name: getattr(obj, field.name) for field in obj._meta.fields}
                for obj in queryset
            ], f)

    write_json("commandes", Order.objects.filter(user=user))
    write_json("locations", Rental.objects.filter(user=user))
    write_json("messages", Message.objects.filter(recipient=user))

    if user.profile_picture and os.path.exists(user.profile_picture.path):
        with open(user.profile_picture.path, "rb") as src:
            with open(os.path.join(temp_dir, os.path.basename(user.profile_picture.name)), "wb") as dst:
                dst.write(src.read())

    for msg in Message.objects.filter(recipient=user):
        if msg.attachment and os.path.exists(msg.attachment.path):
            with open(msg.attachment.path, "rb") as src:
                with open(os.path.join(temp_dir, os.path.basename(msg.attachment.name)), "wb") as dst:
                    dst.write(src.read())

    zip_path = os.path.join(temp_dir, f"{user.username}_data.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file != os.path.basename(zip_path):
                    zipf.write(os.path.join(root, file), arcname=file)

    return FileResponse(open(zip_path, "rb"), as_attachment=True, filename=f"{user.username}_data.zip")
