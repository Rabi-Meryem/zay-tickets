from django.db import models
from django.conf import settings

class Ticket(models.Model):

    STATUS_CHOICES = [
        ('ouvert', 'Ouvert'),
        ('affecte', 'Affecté'),        # superviseur a assigné un agent
        ('en_cours', 'En cours'),      # agent travaille activement
        ('en_attente', 'En attente'),  # attend réponse client/tiers
        ('resolu', 'Résolu'),          # agent a résolu
        ('rouvert', 'Rouvert'),        # client pas satisfait
        ('ferme', 'Fermé'),            # clôture définitive
        ('escalade', 'Escaladé'),      # transféré au superviseur
    ]

    CRITICITE_CHOICES = [
        ('critique', 'Critique'),
        ('haute', 'Haute'),
        ('moyenne', 'Moyenne'),
        ('basse', 'Basse'),
    ]

    CANAL_CHOICES = [
        ('web', 'Portail Web'),
        ('email', 'Email'),
        ('telephone', 'Téléphone'),
    ]

    CATEGORIE_CHOICES = [
        ('reseau', 'Réseau / Connectivité'),
        ('facturation', 'Facturation'),
        ('acces', 'Accès / Authentification'),
        ('bug', 'Bug / Erreur système'),
        ('materiel', 'Matériel / Infrastructure'),
        ('autre', 'Autre'),
    ]

    # ─── INFORMATIONS PRINCIPALES ──────────────────────
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ouvert'
    )
    criticite = models.CharField(
        max_length=20,
        choices=CRITICITE_CHOICES,
        default='moyenne'
    )
    canal = models.CharField(
        max_length=20,
        choices=CANAL_CHOICES,
        default='web'
    )
    categorie = models.CharField(
        max_length=50,
        choices=CATEGORIE_CHOICES,
        default='autre'
    )

    # ─── RELATIONS ─────────────────────────────────────
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tickets_crees'
    )
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets_assignes'
    )

    # ─── MODULE IA ─────────────────────────────────────
    ia_confidence = models.FloatField(null=True, blank=True)

    # ─── SLA ───────────────────────────────────────────
    sla_deadline = models.DateTimeField(null=True, blank=True)
    sla_respecte = models.BooleanField(null=True, blank=True)

    # ─── DATES IMPORTANTES POUR MÉTRIQUES ──────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    affecte_at = models.DateTimeField(
        null=True, blank=True
        # rempli quand status → affecte
        # utilisé pour calculer temps d'affectation
    )
    pris_en_charge_at = models.DateTimeField(
        null=True, blank=True
        # rempli quand status → en_cours
        # temps de réponse = pris_en_charge_at - created_at
    )
    resolu_at = models.DateTimeField(
        null=True, blank=True
        # rempli quand status → resolu
        # temps résolution = resolu_at - created_at
    )
    closed_at = models.DateTimeField(null=True, blank=True)

    # ─── PIÈCES JOINTES ────────────────────────────────
    attachment = models.FileField(
        upload_to='tickets/attachments/',
        null=True,
        blank=True
    )

    # ─── ÉVALUATION CLIENT ─────────────────────────────
    evaluation_note = models.IntegerField(null=True, blank=True)
    evaluation_commentaire = models.TextField(null=True, blank=True)
    evaluation_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"#{self.id} - {self.title} [{self.status}]"


# ─── HISTORIQUE DES CHANGEMENTS DE STATUT ──────────────
class TicketHistorique(models.Model):
    
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name='historique'
    )
    ancien_status = models.CharField(max_length=20)
    nouveau_status = models.CharField(max_length=20)
    modifie_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    commentaire = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket #{self.ticket.id}: {self.ancien_status} → {self.nouveau_status}"