# api/admin.py
from django.contrib import admin
from .models import GroupeElectrogene, Gardien, Action

@admin.register(GroupeElectrogene)
class GroupeElectrogeneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'marque', 'modele', 'autonomie', 'qr_code')
    search_fields = ('nom', 'marque', 'modele')
    readonly_fields = ('qr_code',)

@admin.register(Gardien)
class GardienAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'telephone')
    search_fields = ('nom', 'prenom', 'telephone')

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('groupe', 'etat', 'gardien_on', 'gardien_off', 'heure_allumage', 'heure_extinction', 'temps_ecoule')

    def gardien_on(self, obj):
        return obj.gardien_on if obj.gardien_on else "N/A"

    gardien_on.short_description = 'Gardien qui a allumé'

    def gardien_off(self, obj):
        return obj.gardien_off if obj.gardien_off else "N/A"

    gardien_off.short_description = 'Gardien qui a éteint'

    def heure_allumage(self, obj):
        return obj.heure_allumage.strftime("%Y-%m-%d %H:%M:%S") if obj.heure_allumage else "N/A"
    heure_allumage.short_description = 'Heure d\'allumage'

    def heure_extinction(self, obj):
        return obj.heure_extinction.strftime("%Y-%m-%d %H:%M:%S") if obj.heure_extinction else "N/A"
    heure_extinction.short_description = 'Heure d\'extinction'

    def temps_ecoule(self, obj):
        return obj.temps_ecoule if obj.temps_ecoule else "N/A"
    temps_ecoule.short_description = 'Temps écoulé'
