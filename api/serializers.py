# api/serializers.py
from rest_framework import serializers
from .models import GroupeElectrogene, Gardien, Action

class GroupeElectrogeneSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupeElectrogene
        fields = '__all__'

class GardienSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gardien
        fields = '__all__'

class ActionSerializer(serializers.ModelSerializer):
    previous_on_action_id = serializers.IntegerField(source='previous_on_action.id', read_only=True)
    previous_on_action_timestamp = serializers.DateTimeField(source='previous_on_action.timestamp', format="%Y-%m-%d %H:%M:%S", read_only=True)
    temps_ecoule_formate = serializers.SerializerMethodField()
    gardien_on_nom = serializers.CharField(source='gardien_on.nom', read_only=True)
    gardien_on_prenom = serializers.CharField(source='gardien_on.prenom', read_only=True)
    gardien_off_nom = serializers.CharField(source='gardien_off.nom', read_only=True)
    gardien_off_prenom = serializers.CharField(source='gardien_off.prenom', read_only=True)

    class Meta:
        model = Action
        fields = [
            'groupe', 'etat', 'timestamp', 'heure_allumage', 'heure_extinction',
            'temps_ecoule', 'temps_ecoule_formate', 'previous_on_action_id',
            'previous_on_action_timestamp', 'gardien_on_nom', 'gardien_on_prenom',
            'gardien_off_nom', 'gardien_off_prenom'
        ]

    def get_temps_ecoule_formate(self, obj):
        if obj.etat == 'OFF' and obj.temps_ecoule:
            total_seconds = int(obj.temps_ecoule.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours}:{minutes:02}:{seconds:02}"
        return None
