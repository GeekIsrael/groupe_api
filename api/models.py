# api/models.py
import uuid
from django.db import models
from django.utils import timezone

class GroupeElectrogene(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # UUID unique
    qr_code = models.CharField(max_length=100, editable=False)  # Champ QR code contenant l'UUID
    nom = models.CharField(max_length=100)
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    autonomie = models.DecimalField(max_digits=5, decimal_places=2)  # Autonomie en heures

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.qr_code = str(self.id)  # Assigner l'UUID au champ `qr_code`
        super().save(*args, **kwargs)
    
    @classmethod
    def get_all_brands(cls):
        return cls.objects.values_list('marque', flat=True).distinct()

    def __str__(self):
        return f"{self.nom} - {self.marque} {self.modele}"

#----------------------------------------------------------------------------------

class Gardien(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    telephone = models.CharField(max_length=15, unique=True)
    groupe_associe = models.ForeignKey('GroupeElectrogene', null=True, blank=True, on_delete=models.SET_NULL, related_name="gardiens")

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    
#---------------------------------------------------------------------------------------------

from django.db import models
from django.utils import timezone

from django.db import models
from django.utils import timezone

class Action(models.Model):
    ETAT_CHOICES = [
        ('ON', 'Allumé'),
        ('OFF', 'Éteint')
    ]
    
    groupe = models.ForeignKey(GroupeElectrogene, on_delete=models.CASCADE, related_name='actions')
    etat = models.CharField(max_length=3, choices=ETAT_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)  # Enregistre l'heure de l'action
    heure_allumage = models.DateTimeField(null=True, blank=True)  # Heure d'allumage pour les actions ON
    heure_extinction = models.DateTimeField(null=True, blank=True)  # Heure d'extinction pour les actions OFF
    temps_ecoule = models.DurationField(null=True, blank=True)  # Temps écoulé entre ON et OFF
    previous_on_action = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='next_off_actions')
    
    # Nouveau champ pour stocker le gardien qui a allumé le groupe
    gardien_on = models.ForeignKey(Gardien, null=True, blank=True, on_delete=models.SET_NULL, related_name='actions_allumage', verbose_name='Gardien qui a allumé')
    gardien_off = models.ForeignKey(Gardien, null=True, blank=True, on_delete=models.SET_NULL, related_name='actions_extinction', verbose_name='Gardien qui a éteint')

    def save(self, *args, **kwargs):
        gardien = kwargs.pop('gardien', None)

        if self.etat == 'ON':
            self.heure_allumage = timezone.now()
            self.heure_extinction = None
            self.temps_ecoule = None
            self.previous_on_action = None
            self.gardien_on = gardien  # Assigner le gardien lors de l'allumage

        elif self.etat == 'OFF':
            last_on_action = Action.objects.filter(groupe=self.groupe, etat='ON').order_by('-timestamp').first()
            if last_on_action:
                self.previous_on_action = last_on_action
                self.heure_extinction = timezone.now()
                self.temps_ecoule = self.heure_extinction - last_on_action.heure_allumage
                self.heure_allumage = last_on_action.heure_allumage
                self.gardien_off = gardien  # Associe le gardien de l'action OFF
                self.gardien_on = last_on_action.gardien_on  # Associe le gardien de l'action ON
            else:
                # Pas d'action ON précédente, gérer ce cas
                self.heure_extinction = None
                self.temps_ecoule = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.groupe.nom} - {self.get_etat_display()} at {self.timestamp}"