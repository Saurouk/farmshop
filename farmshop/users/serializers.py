from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Message

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    admin_contact = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile_picture', 'admin_contact']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """ Crée un utilisateur avec un mot de passe sécurisé """
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)  # Hash du mot de passe
        user.save()
        return user

    def update(self, instance, validated_data):
        """ Mise à jour du profil utilisateur (incluant le mot de passe et la photo) """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # Hash du nouveau mot de passe
        instance.save()
        return instance

    def get_admin_contact(self, obj):
        """ Récupère les informations de contact de l'admin """
        admin = User.objects.filter(is_staff=True).first()
        if admin:
            return {"username": admin.username, "email": admin.email}
        return None

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field='username', read_only=True)
    recipient = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'is_read', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']
