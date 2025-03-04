from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Message

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    admin_contact = serializers.SerializerMethodField()
    inbox = serializers.SerializerMethodField()  # ✅ Ajout de la boîte de réception
    password = serializers.CharField(write_only=True, required=False)  # ✅ Conserver la gestion du mot de passe

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile_picture', 'admin_contact', 'inbox']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """ ✅ Crée un utilisateur avec un mot de passe sécurisé """
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)  # Hash du mot de passe
        user.save()
        return user

    def update(self, instance, validated_data):
        """ ✅ Mise à jour du profil utilisateur (mot de passe & photo) """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # Hash du nouveau mot de passe
        instance.save()
        return instance

    def get_admin_contact(self, obj):
        """ ✅ Récupère les informations de contact de l'admin """
        admin = User.objects.filter(is_staff=True).first()
        if admin:
            return {"username": admin.username, "email": admin.email}
        return None

    def get_inbox(self, obj):
        """ ✅ Récupère la boîte de réception de l'utilisateur """
        messages = Message.objects.filter(recipient=obj).order_by('-created_at')
        return MessageSerializer(messages, many=True).data

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field='username', read_only=True)
    recipient = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'is_read', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']
