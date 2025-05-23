from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Message

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    admin_contact = serializers.SerializerMethodField()
    inbox = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password',
            'profile_picture', 'bio', 'wants_newsletter',
            'is_staff', 'admin_contact', 'inbox'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    def get_admin_contact(self, obj):
        admin = User.objects.filter(is_staff=True).first()
        if admin:
            return {"username": admin.username, "email": admin.email}
        return None

    def get_inbox(self, obj):
        messages = Message.objects.filter(recipient=obj).order_by('-created_at')
        return MessageSerializer(messages, many=True).data


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(slug_field='username', read_only=True)
    recipient = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    attachment = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'is_read', 'created_at', 'attachment']
        read_only_fields = ['id', 'sender', 'created_at']


class AdminDashboardSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    total_products = serializers.IntegerField()
    total_articles = serializers.IntegerField()
    total_reports = serializers.IntegerField()
