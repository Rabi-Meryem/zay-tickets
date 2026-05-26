from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('agent', 'Agent'),
        ('superviseur', 'Superviseur'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='client'
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    
    created_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users_crees'
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"