
from rest_framework import exceptions, serializers
from .models import User
from allauth.account.admin import EmailAddress

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
