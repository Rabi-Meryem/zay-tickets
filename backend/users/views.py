from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django_ratelimit.decorators import ratelimit

from .models import CustomUser
from .serializers import (
    UserSerializer,
    CreateUserSerializer,
    LoginSerializer,
    ChangePasswordSerializer
)
from .permissions import IsAdmin, IsAdminOrSuperviseur


@api_view(['POST'])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def login_view(request):
    """
    POST /api/auth/login
    Corps : { "email": "...", "password": "..." }
    Retourne : { access, refresh, user }
    """
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    # chercher l'utilisateur par email
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response(
            {'error': 'Email ou mot de passe incorrect'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # vérifier le mot de passe
    if not user.check_password(password):
        return Response(
            {'error': 'Email ou mot de passe incorrect'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # vérifier que le compte est actif
    if not user.is_active:
        return Response(
            {'error': 'Compte désactivé. Contactez l\'administrateur'},
            status=status.HTTP_403_FORBIDDEN
        )

    # générer les tokens JWT
    refresh = RefreshToken.for_user(user)

    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    POST /api/auth/logout
    Blackliste le refresh token
    """
    try:
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(
            {'message': 'Déconnexion réussie'},
            status=status.HTTP_200_OK
        )
    except Exception:
        return Response(
            {'error': 'Token invalide'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """
    GET /api/auth/me
    Retourne les infos de l'utilisateur connecté
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAdmin])
def users_list_view(request):
    """
    GET  /api/users/ → liste tous les utilisateurs (admin)
    POST /api/users/ → créer un utilisateur (admin)
    """
    if request.method == 'GET':
        users = CustomUser.objects.all().order_by('-date_joined')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CreateUserSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAdmin])
def user_detail_view(request, pk):
    """
    GET    /api/users/<id>/ → voir un utilisateur
    PUT    /api/users/<id>/ → modifier
    DELETE /api/users/<id>/ → désactiver (pas supprimer)
    """
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(
            {'error': 'Utilisateur introuvable'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        return Response(UserSerializer(user).data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = UserSerializer(
            user,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':
        # on désactive le compte, on ne supprime pas
        user.is_active = False
        user.save()
        return Response(
            {'message': f'Compte de {user.username} désactivé'},
            status=status.HTTP_200_OK
        )