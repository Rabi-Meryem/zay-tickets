from django.db import models
from django.conf import settings
class Message(models.Model):

    TYPE_CHOICES = [
        ('public', 'Public'),
        ('interne', 'Note interne'),
    ]

    ticket = models.ForeignKey(
        'tickets.Ticket',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages_envoyes'
    )
    contenu = models.TextField()
    type_message = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='public'
    )
    lu = models.BooleanField(default=False)
    attachment = models.FileField(
        upload_to='messages/attachments/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message de {self.auteur} sur ticket #{self.ticket.id}"