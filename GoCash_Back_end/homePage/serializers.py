from rest_framework import serializers
from users.models import User


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=50)
    phone_number = serializers.CharField(required=True, max_length=15)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True, min_length=8)

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError("Username is required.")
        return value

    def validate_phone_number(self, value):
        wrong_format = '[A/+*^%$#@!]()+_-<>{}'
        if not value:
            raise serializers.ValidationError("Phone number is required.")
        if value in wrong_format:
            raise serializers.ValidationError("Wrong Phone number format \"must be numbers only\"")
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number is already registered.")
        return value


class SigninSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, max_length=15)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True, min_length=8)

    def validate_phone_number(self, value):
        if not value:
            raise serializers.ValidationError("Phone number is required.")
        try:
            user = User.objects.get(phone_number=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this phone number does not exist.")
        self.context['user'] = user
        return value

    def validate_password(self, value):
        user = self.context.get('user')
        if value and not user.check_password(value):
            raise serializers.ValidationError("Incorrect password.")
        return value

    def to_representation(self, instance):
        user = self.context.get('user')
        return {
            'username': user.username,
            'phone_number': user.phone_number,
            'subscription_plan': user.subscription_plan.name if user.subscription_plan else None,
            'token': instance.key
        }
