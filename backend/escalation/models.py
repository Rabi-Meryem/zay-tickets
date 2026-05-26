from django.db import models
from django.conf import settings

class Escalation(models.Model):

    TYPE_CHOICES = [
        ('manuelle', 'Manuelle'),
        ('automatique_sla', 'Automatique — SLA dépassé'),
        ('automatique_critique', 'Automatique — Ticket critique non pris en charge'),
        ('automatique_rouvert', 'Automatique — Ticket rouvert plusieurs fois'),
    ]

    STATUT_CHOICES = [
        ('en_attente', 'En attente de traitement'),
        ('prise_en_charge', 'Prise en charge par superviseur'),
        ('resolue', 'Résolue'),
    ]

    # ─── QUEL TICKET ───────────────────────────────────
    ticket = models.ForeignKey(
        'tickets.Ticket',
        on_delete=models.CASCADE,
        related_name='escalations'
    )

    # ─── QUI A ESCALADÉ ────────────────────────────────
    escalade_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='escalations_declenchees'
    )

    # ─── VERS QUI ──────────────────────────────────────
    escalade_vers = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='escalations_recues'
    )

    # ─── TYPE ──────────────────────────────────────────
    type_escalade = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        default='manuelle'
    )

    # ─── MOTIF TEXTE LIBRE ─────────────────────────────
    motif = models.TextField()
    # l'agent écrit librement et en détail
    # pas de limite, pas de liste fixe

    # ─── STATUT ────────────────────────────────────────
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente'
    )

    # ─── COMMENTAIRE SUPERVISEUR ───────────────────────
    commentaire_superviseur = models.TextField(
        null=True,
        blank=True
        # le superviseur explique ce qu'il a fait
    )

    # ─── DATES ─────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    prise_en_charge_at = models.DateTimeField(null=True, blank=True)
    resolue_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Escalade ticket #{self.ticket.id} — {self.type_escalade} — {self.statut}"