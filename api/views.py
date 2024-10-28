# api/views.py
from .models import GroupeElectrogene, Gardien, Action
from .serializers import GroupeElectrogeneSerializer, GardienSerializer, ActionSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .utils import calculer_temps_utilisation


@api_view(['GET', 'POST'])
def liste_groupes(request):
    if request.method == 'GET':
        groupes = GroupeElectrogene.objects.all()
        serializer = GroupeElectrogeneSerializer(groupes, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = GroupeElectrogeneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def details_groupe(request, pk):
    try:
        groupe = GroupeElectrogene.objects.get(pk=pk)
    except GroupeElectrogene.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GroupeElectrogeneSerializer(groupe)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = GroupeElectrogeneSerializer(groupe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        groupe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#---------------------------- Gestion des gardiens ------------------------------------
@api_view(['GET', 'POST'])
def liste_gardiens(request):
    if request.method == 'GET':
        gardiens = Gardien.objects.all()
        serializer = GardienSerializer(gardiens, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = GardienSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def details_gardien(request, pk):
    try:
        gardien = Gardien.objects.get(pk=pk)
    except Gardien.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GardienSerializer(gardien)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = GardienSerializer(gardien, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        gardien.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#--------------------------------------------------------------------------------------
@api_view(['POST'])
def enregistrer_gardien(request):
    groupe_uuid = request.data.get("groupe_uuid")  # Récupérer l'UUID du groupe à partir des données

    try:
        groupe = GroupeElectrogene.objects.get(id=groupe_uuid)  # Utilisez id ici car vous avez défini `id` comme UUID
    except GroupeElectrogene.DoesNotExist:
        return Response({"error": "Groupe introuvable."}, status=status.HTTP_404_NOT_FOUND)

    nom = request.data.get("nom")
    prenom = request.data.get("prenom")
    telephone = request.data.get("telephone")

    # Création du gardien avec association au groupe
    gardien, created = Gardien.objects.update_or_create(
        telephone=telephone,
        defaults={"nom": nom, "prenom": prenom, "groupe_associe": groupe}
    )
    
    serializer = GardienSerializer(gardien)
    return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)



@api_view(['POST'])
def toggle_groupe_etat(request, groupe_id):
    try:
        groupe = GroupeElectrogene.objects.get(id=groupe_id)
    except GroupeElectrogene.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    telephone = request.data.get("telephone")

    try:
        gardien = Gardien.objects.get(telephone=telephone)
    except Gardien.DoesNotExist:
        return Response({"error": "Le gardien n'est pas associé à ce groupe."}, status=status.HTTP_403_FORBIDDEN)

    etat = request.data.get("etat")
    if etat not in ['ON', 'OFF']:
        return Response({"error": "État invalide."}, status=status.HTTP_400_BAD_REQUEST)

    if etat == 'ON':
        # Création de l'action pour le groupe par le gardien
        action = Action(groupe=groupe, etat=etat)
        action.save(gardien=gardien)  # Sauvegarde avec le gardien pour ON
        serializer = ActionSerializer(action)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    elif etat == 'OFF':
        # Création d'une nouvelle action pour l'extinction
        action = Action(groupe=groupe, etat=etat)
        action.save(gardien=gardien)  # Sauvegarde avec le gardien pour OFF

        # Sérialiser l'action mise à jour
        serializer = ActionSerializer(action)
        return Response(serializer.data, status=status.HTTP_200_OK)


#---------------------------- Log des actiosns par jour -----------------

@api_view(['GET'])
def logs_par_jour(request):
    date_str = request.query_params.get('date')  # Attendez une date sous forme de chaîne (YYYY-MM-DD)
    
    if not date_str:
        return Response({"error": "Date requise."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Convertir la chaîne en objet date
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return Response({"error": "Format de date invalide. Utilisez YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    # Récupérer toutes les actions pour la date spécifiée
    actions = Action.objects.filter(timestamp__date=date)

    # Sérialiser les actions
    serializer = ActionSerializer(actions, many=True)
    
    return Response(serializer.data)

#------------ Une fonction de notification -------------------------------

@api_view(['GET'])
def obtenir_temps_utilisation(request, groupe_uuid):
    try:
        groupe = GroupeElectrogene.objects.get(id=groupe_uuid)
    except GroupeElectrogene.DoesNotExist:
        return Response({"error": "Groupe introuvable."}, status=status.HTTP_404_NOT_FOUND)

    temps_utilisation = calculer_temps_utilisation(groupe)
    return Response({"temps_utilisation": str(temps_utilisation)}, status=status.HTTP_200_OK)

#------------------------------- Bilan de groupes --------------------------------------
def format_temps_restant(temps_restant):
    jours = temps_restant.days
    heures, reste_secondes = divmod(temps_restant.seconds, 3600)
    minutes, secondes = divmod(reste_secondes, 60)
    return f"{jours} jours {heures:02d}h:{minutes:02d}min:{secondes:02d}sec"

@api_view(['GET'])
def bilan_groupes(request):
    data = []

    for groupe in GroupeElectrogene.objects.all():
        actions_journalieres = Action.objects.filter(groupe=groupe, timestamp__date=timezone.now().date())
        temps_total = timedelta()  # Initialisation du temps total

        for action in actions_journalieres:
            if action.etat == 'ON' and action.temps_ecoule:
                temps_total += action.temps_ecoule

        # Calcul de l'autonomie restante
        autonomie = timedelta(hours=float(groupe.autonomie))
        temps_restant = autonomie - temps_total
        
        # Message de seuil
        seuil_message = "le groupe a encore d'autonomie " if temps_restant > timedelta(hours=1) else "Bientôt le seuil pour la vidange"

        # Formatage des données pour chaque groupe
        data.append({
            "groupe": {
                "nom": groupe.nom,
                "marque": groupe.marque,
                "modele": groupe.modele,
                "autonomie_heures": float(groupe.autonomie)
            },
            "temps_total_journalier": str(temps_total),  # Format hh:mm:ss
            "temps_restant": format_temps_restant(temps_restant) if temps_restant > timedelta(0) else "00:00:00",  # Format hh:mm:ss
            "seuil_message": seuil_message
        })

    return Response(data)

#-------------------- Cette fonction renvoie toutes les marques des groupes electrogene-------------
@api_view(['GET'])
def get_group_brands(request):
    marques = GroupeElectrogene.get_all_brands()
    return Response({"marques": list(marques)})