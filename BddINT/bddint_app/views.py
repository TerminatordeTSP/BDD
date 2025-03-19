from django.shortcuts import render, redirect
from django.contrib import messages
from bddint_app.forms import LoginForm,CamionForm,ChauffeurForm,LocalisationForm
from bddint_app.forms import RequetteForm
from bddint_app.models import Logins, Camion, Chauffeur
from mysql.connector import IntegrityError
from django.shortcuts import render, redirect
from django.db import connection  # Import pour exécuter des requêtes SQL
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login  # Ajoute un alias si nécessaire
from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
import mysql.connector

from django.shortcuts import render, redirect
from django.http import HttpResponse
import mysql.connector
from .models import Logins

def vue_affectation_chauffeur(request):
    if 'user_login' in request.session:
        user_login = request.session.get('user_login', 'Utilisateur inconnu')

        try:
            user = Logins.objects.get(login=user_login)

            if role(request) == "Chauffeur":
                try:
                    # Connexion à MySQL avec les identifiants de l'utilisateur connecté
                    conn = mysql.connector.connect(
                        host="127.0.0.1",
                        port=8889,
                        user=user.login,  # Connexion en tant que l'utilisateur spécifique
                        password=user.mot_de_passe,
                        database="Gestion d’une flotte de camions"
                    )
                    cursor = conn.cursor()

                    # Exécution de la requête SQL avec l'utilisateur spécifique
                    query = "SELECT * FROM `Gestion d’une flotte de camions`.`vue_affectations_chauffeur`"
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    print(rows)

                    # Fermeture des connexions
                    cursor.close()
                    conn.close()

                    return render(request, 'vue_affectations_chauffeur.html', {'login': user_login, 'result': rows})

                except mysql.connector.Error as e:
                    return HttpResponse(f"Erreur SQL : {e}", status=500)

            else:
                return render(request, 'denied3.html')

        except Logins.DoesNotExist:
            return HttpResponse("Utilisateur introuvable.", status=404)

    return redirect('login')  # Redirige si l'utilisateur n'est pas connecté

def vue_logisticien(request):
    if 'user_login' in request.session:
        user_login = request.session.get('user_login', 'Utilisateur inconnu')

        try:
            user = Logins.objects.get(login=user_login)

            if role(request) == "Logisticien":
                try:
                    # Exécution de la requête SQL avec l'utilisateur spécifique
                    query = "SELECT * FROM `Gestion d’une flotte de camions`.`vue_synthese_logistique`"
                    with connection.cursor() as cursor:
                        cursor.execute(query)
                        rows = cursor.fetchall()

                    # Fermeture des connexions
                    cursor.close()
                    print(rows)

                    return render(request, 'vue_logisticien.html', {'login': user_login, 'result': rows})

                except mysql.connector.Error as e:
                    return HttpResponse(f"Erreur SQL : {e}", status=500)

            else:
                return render(request, 'denied4.html')

        except Logins.DoesNotExist:
            return HttpResponse("Utilisateur introuvable.", status=404)

    return redirect('login')  # Redirige si l'utilisateur n'est pas connecté

def role(request):
    if 'user_login' in request.session:
        user_login = request.session.get('user_login', 'Utilisateur inconnu')  #
        user = Logins.objects.get(login=user_login)
        role = user.role
        return role

def camions_insert(request):
    user_login = request.session.get('user_login', 'Utilisateur inconnu')
    if role(request) == "root":
        if request.method == 'POST':
            # créer une instance de notre formulaire et le remplir avec les données POST
            form = CamionForm(request.POST)
        else:
            # ceci doit être une requête GET, donc créer un formulaire vide
            form = CamionForm()
        if form.is_valid():
            poid_total_transportable_kg = form.cleaned_data['poid_total_transportable_kg']
            type = form.cleaned_data['type']
            numéro_d_immatriculation = form.cleaned_data['numéro_d_immatriculation']
            try:
                if Camion.objects.filter(numéro_d_immatriculation=numéro_d_immatriculation).exists():
                    form.add_error(None, f"Erreur : un camion avec le numéro_d_immatriculation '{numéro_d_immatriculation}' existe déjà.")
                else:
                    camion = Camion(numéro_d_immatriculation=numéro_d_immatriculation, type=type, poid_total_transportable_kg=poid_total_transportable_kg)
                    camion.save()
                    return camions(request)
            except IntegrityError as e:
                form.add_error(None,f"Erreur : un camion avec le numéro_d_immatriculation '{numéro_d_immatriculation}' existe déjà.")

        return render(request,
                      'camions_update.html',
                      {'form': form})
    else:
        return render(request, 'denied.html')
def camions_update(request, id):
    user_login = request.session.get('user_login', 'Utilisateur inconnu')
    if role(request) == "root":
        camion = get_object_or_404(Camion, numéro_d_immatriculation=id)
        if request.method == 'POST':
            form = CamionForm(request.POST, instance=camion)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, 'Camion modifié avec succès.')
                    return redirect('camions')
                except Exception as e:
                    messages.error(request, f'Erreur lors de la modification: {str(e)}')
        else:
            form = CamionForm(instance=camion)

        return render(request,
                      'camions_update.html',
                      {'form': form, 'camions': camion})
    else:
        return render(request, 'denied.html')
def camions(request):
    if 'user_login' in request.session:
        user_login = request.session.get('user_login', 'Utilisateur inconnu')
        if role(request)=="root":
            camions = Camion.objects.all()
            return render(request, 'camions.html',{'login': user_login, 'result': camions})
        else :
            return render(request, 'denied.html')

    else:
        return redirect('login')

def chauffeurs_update(request, numéro_de_permis_de_conduire):
    user_login = request.session.get('user_login', 'Utilisateur inconnu')
    if role(request) == "root":
        chauffeur = get_object_or_404(Chauffeur, numéro_de_permis_de_conduire=numéro_de_permis_de_conduire)
        if request.method == 'POST':
            form = ChauffeurForm(request.POST, instance=chauffeur)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, 'Chauffeur modifié avec succès.')
                    return redirect('chauffeurs')
                except Exception as e:
                    messages.error(request, f'Erreur lors de la modification: {str(e)}')
        else:
            form = ChauffeurForm(instance=chauffeur)

        return render(request,
                      'chauffeur_update.html',
                      {'form': form, 'chauffeur': chauffeur})
    else:
        return render(request, 'denied.html')

def chauffeurs(request):
    if 'user_login' in request.session:
        user_login = request.session.get('user_login', 'Utilisateur inconnu')
        if role(request)!="Chauffeur":
            Chauffeurs = Chauffeur.objects.all()
            return render(request, 'chauffeurs.html',{'login': user_login, 'result': Chauffeurs})
        else :
            return render(request, 'denied2.html')

    else:
        return redirect('login')

def chauffeurs_delete(request, numéro_de_permis_de_conduire):
    user_login = request.session.get('user_login', 'Utilisateur inconnu')
    if role(request) == "root":
        chauffeur = get_object_or_404(Chauffeur, numéro_de_permis_de_conduire=numéro_de_permis_de_conduire)
        chauffeur.delete()

        return chauffeurs(request)
    else:
        return render(request, 'denied.html')

def requettes(request):
    if 'user_login' in request.session:
        user_login = request.session.get('user_login', 'Utilisateur inconnu')
        if role(request)=="root":
            if request.method == 'POST':
                form = RequetteForm(request.POST)
                if form.is_valid():
                    # Récupérer les données saisies par l'utilisateur
                    type = form.cleaned_data['type_de_camion']
                    ville = form.cleaned_data['ville_d_arrivée']
                    query = """
                        SELECT c.numéro_d_immatriculation AS plaque, c.type, m.nom AS marchandise, m.ville_de_départ
                        FROM Camion c
                        JOIN Marchandise m ON m.numéro_d_immatriculation = c.numéro_d_immatriculation
                        WHERE c.type = %s
                        AND m.ville_d_arrivée = %s;
                        """
                    # Exécuter la requête avec les paramètres
                    with connection.cursor() as cursor:
                        cursor.execute(query, [type, ville])
                        rows = cursor.fetchall()
                    return render(request, 'requettes.html', {'form': form,'result': rows})
            else:
                form = RequetteForm()

            return render(request, 'requettes.html',{'login': user_login, 'form': form})
        else :
            return render(request, 'denied.html')

    else:
        return redirect('login')



def home(request):
    if 'user_login' in request.session:
        user_login = request.session.get('user_login', 'Utilisateur inconnu')
        if role(request)=="Chauffeur":
            return render(request, 'home_chauffeur.html', {'login': user_login})
        if role(request)=="Logisticien":
            return render(request, 'home_logisticien.html', {'login': user_login})
        else :
            return render(request, 'home_root.html', {'login': user_login})

    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Récupérer les données saisies par l'utilisateur
            username = form.cleaned_data['login']
            password = form.cleaned_data['mot_de_passe']

            # Vérifier dans la table Logins si ce couple username/password existe
            try:
                user = Logins.objects.get(login=username, mot_de_passe=password)
                request.session['user_login'] = user.login  # Stocker le login dans la session
                return redirect('home')
            except Logins.DoesNotExist:
                # Si l'utilisateur n'existe pas dans la base de données
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    # Supprimer l'utilisateur de la session pour le déconnecter
    if 'user_login' in request.session:
        del request.session['user_login']
        request.session.modified = True # Forcer l'enregistrement des modifications de la session
        # Rediriger vers la page de connexion
    return redirect('login')


def localisation(request):
    if 'user_login' in request.session:
        user_login = request.session.get('user_login', 'Utilisateur inconnu')
        if role(request)=="root":
            if request.method == 'POST':
                form = LocalisationForm(request.POST)
                if form.is_valid():
                    # Récupérer les données saisies par l'utilisateur
                    type = form.cleaned_data['type']
                    date = form.cleaned_data['date']
                    query = """
                        SELECT c.numéro_d_immatriculation, m.ville_de_départ, m.ville_d_arrivée
                        FROM Camion c
                        JOIN Marchandise m ON c.numéro_d_immatriculation = m.numéro_d_immatriculation
                        WHERE c.type = %s 
                        AND m.date_de_transport = %s;
                        """
                    # Exécuter la requête avec les paramètres
                    with connection.cursor() as cursor:
                        cursor.execute(query, [type, date])
                        rows = cursor.fetchall()
                    return render(request, 'localisation.html', {'form': form,'result': rows})
            else:
                form = LocalisationForm()

            return render(request, 'localisation.html',{'login': user_login, 'form': form})
        else :
            return render(request, 'denied2.html')

    else:
        return redirect('login')







