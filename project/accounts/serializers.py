from allauth.account.admin import EmailAddress
from rest_framework import serializers

from .models import User


class UserDetailsSerializer(serializers.ModelSerializer):
    verified = serializers.SerializerMethodField()

    def get_verified(self, obj):
        user_emails = EmailAddress.objects.filter(user=obj)
        if user_emails:
            return user_emails[0].verified
        else:
            return False

    class Meta:
        model = User
        fields = ("email", "verified")
