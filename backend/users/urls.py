from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentification
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', views.me_view, name='me'),

    # Gestion utilisateurs (admin)
    path('users/', views.users_list_view, name='users_list'),
    path('users/<int:pk>/', views.user_detail_view, name='user_detail'),
]