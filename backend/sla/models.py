from django.db import models

class SLAConfig(models.Model):
    
    CRITICITE_CHOICES = [
        ('critique', 'Critique'),
        ('haute', 'Haute'),
        ('moyenne', 'Moyenne'),
        ('basse', 'Basse'),
    ]
    
    criticite = models.CharField(
        max_length=20,
        choices=CRITICITE_CHOICES,
        unique=True
    )
    delai_heures = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.criticite} → {self.delai_heures}h"