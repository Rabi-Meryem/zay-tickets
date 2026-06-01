from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'admin'
        )

class IsSuperviseur(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'superviseur'
        )

class IsAgent(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'agent'
        )

class IsClient(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'client'
        )

class IsAdminOrSuperviseur(BasePermission):
    """Admin OU Superviseur peuvent accéder"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in ['admin', 'superviseur']
        )

class IsAgentOrSuperviseur(BasePermission):
    """Agent OU Superviseur peuvent accéder"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in ['agent', 'superviseur']
        )