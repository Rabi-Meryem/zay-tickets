from django.db import models
from django.conf import settings

class Report(models.Model):

    TYPE_CHOICES = [
        ('performance', 'Rapport de performance'),
        ('sla', 'Rapport SLA'),
        ('activite', 'Rapport d activité'),
        ('agents', 'Rapport agents'),
        ('satisfaction', 'Rapport satisfaction clients'),
    ]

    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
    ]

    PERIODICITE_CHOICES = [
        ('hebdomadaire', 'Hebdomadaire'),
        ('mensuelle', 'Mensuelle'),
        ('personnalise', 'Personnalisé'),
    ]

    STATUT_CHOICES = [
        ('en_cours', 'Génération en cours'),
        ('termine', 'Terminé'),
        ('erreur', 'Erreur de génération'),
    ]

    # ─── QUI A GÉNÉRÉ ──────────────────────────────────
    genere_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reports_generes'
        # le superviseur qui a demandé le rapport
    )

    # ─── TYPE ET FORMAT ────────────────────────────────
    type_rapport = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES
    )

    format_fichier = models.CharField(
        max_length=10,
        choices=FORMAT_CHOICES
    )

    periodicite = models.CharField(
        max_length=20,
        choices=PERIODICITE_CHOICES,
        default='mensuelle'
    )

    # ─── PÉRIODE COUVERTE ──────────────────────────────
    date_debut = models.DateField()
    # début de la période du rapport
    # ex: 01/05/2026

    date_fin = models.DateField()
    # fin de la période du rapport
    # ex: 31/05/2026

    # ─── FICHIER GÉNÉRÉ ────────────────────────────────
    fichier = models.FileField(
        upload_to='reports/',
        null=True,
        blank=True
        # null tant que la génération n'est pas terminée
        # rempli par Celery après génération
    )

    # ─── STATUT GÉNÉRATION ─────────────────────────────
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_cours'
        # en_cours → Celery est en train de générer
        # termine  → fichier prêt à télécharger
        # erreur   → génération échouée
    )

    # ─── DATES ─────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    
    termine_at = models.DateTimeField(
        null=True,
        blank=True
        # quand Celery a fini de générer le fichier
    )

    def __str__(self):
        return f"Rapport {self.type_rapport} {self.format_fichier} — {self.periodicite}"