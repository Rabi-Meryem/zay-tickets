from django.db import models
from django.conf import settings

class Notification(models.Model):

    TYPE_CHOICES = [
        # ── CLIENT ──────────────────────────────
        ('ticket_cree', 'Ticket créé'),
        ('ticket_affecte', 'Ticket affecté à un agent'),
        ('ticket_statut_change', 'Statut ticket modifié'),
        ('ticket_resolu', 'Ticket résolu'),
        ('message_recu', 'Nouveau message reçu'),

        # ── AGENT ───────────────────────────────
        ('ticket_assigne', 'Nouveau ticket assigné'),
        ('sla_alerte', 'Alerte SLA — approche dépassement'),
        ('sla_depasse', 'SLA dépassé'),
        ('priorite_modifiee', 'Priorité ticket modifiée'),

        # ── SUPERVISEUR ─────────────────────────
        ('escalade_recue', 'Ticket escaladé reçu'),
        ('sla_depasse_superviseur', 'SLA dépassé — intervention requise'),
        ('surcharge_agent', 'Alerte surcharge agent'),

        # ── ADMIN ───────────────────────────────
        ('erreur_systeme', 'Erreur critique système'),
        ('echec_smtp', 'Échec intégration SMTP/IMAP'),
        ('anomalie_securite', 'Anomalie de sécurité détectée'),
    ]

    CANAL_CHOICES = [
        ('inapp', 'Notification in-app'),
        ('email', 'Email'),
        ('both', 'In-app + Email'),
    ]

    # ─── QUI REÇOIT LA NOTIFICATION ────────────────────
    destinataire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
        # chaque notification appartient à un utilisateur
    )

    # ─── QUEL TICKET CONCERNÉ ──────────────────────────
    ticket = models.ForeignKey(
        'tickets.Ticket',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications'
        # null pour les notifications système (erreur smtp...)
        # rempli pour les notifications liées à un ticket
    )

    # ─── TYPE ET CONTENU ───────────────────────────────
    type_notification = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES
    )

    titre = models.CharField(max_length=255)
    # ex: "Ticket #5 résolu"

    message = models.TextField()
    # ex: "Votre ticket #5 — Bug login a été résolu
    #      par l'agent Khalid. Merci d'évaluer la résolution."

    # ─── CANAL D'ENVOI ─────────────────────────────────
    canal = models.CharField(
        max_length=10,
        choices=CANAL_CHOICES,
        default='both'
        # par défaut on envoie in-app + email
    )

    # ─── STATUT LECTURE ────────────────────────────────
    lu = models.BooleanField(default=False)
    # False = non lu → badge rouge dans l'interface
    # True  = lu → notification grisée

    lu_at = models.DateTimeField(
        null=True,
        blank=True
        # quand l'utilisateur a lu la notification
    )

    # ─── DATE ──────────────────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        # les plus récentes en premier

    def __str__(self):
        return f"Notif {self.type_notification} → {self.destinataire} | lu: {self.lu}"