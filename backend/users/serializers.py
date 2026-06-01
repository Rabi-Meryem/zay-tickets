from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """Serializer pour afficher les infos d'un utilisateur"""
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email',
            'first_name', 'last_name',
            'role', 'phone', 'is_active',
            'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer pour créer un utilisateur (admin uniquement)"""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email',
            'first_name', 'last_name',
            'role', 'phone', 'password'
        ]

    def create(self, validated_data):
        # create_user hache automatiquement le mot de passe
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'client'),
            phone=validated_data.get('phone', ''),
            password=validated_data['password']
        )
        # enregistrer qui a créé ce compte
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user.created_by = request.user
            user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer pour le login"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer pour changer le mot de passe"""
    ancien_password = serializers.CharField(write_only=True)
    nouveau_password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )