from rest_framework import serializers
from .models import ContactMessage

class ContactMessageSerializer(serializers.ModelSerializer):
    reason_display = serializers.SerializerMethodField()

    class Meta:
        model = ContactMessage
        fields = [
            'id',
            'email',
            'subject',
            'content',
            'reason',
            'reason_display',
            'is_handled',
            'response',
            'created_at',
            'responded_at',
        ]
        read_only_fields = ['is_handled', 'response', 'created_at', 'responded_at']

    def get_reason_display(self, obj):
        reasons = {
            'products': {
                'fr': "Nos produits",
                'en': "Our products"
            },
            'articles': {
                'fr': "Nos articles",
                'en': "Our articles"
            },
            'other': {
                'fr': "Autres",
                'en': "Other"
            }
        }
        lang = self.context.get('request').headers.get('Accept-Language', 'fr')[:2]
        return reasons.get(obj.reason, {}).get(lang, obj.get_reason_display())
