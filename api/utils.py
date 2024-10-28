from datetime import timedelta
from .models import Action

def calculer_temps_utilisation(groupe):
    actions = Action.objects.filter(groupe=groupe)
    temps_total = timedelta()

    for action in actions:
        if action.etat == 'ON' and action.heure_extinction:
            temps_total += action.temps_ecoule

    return temps_total
