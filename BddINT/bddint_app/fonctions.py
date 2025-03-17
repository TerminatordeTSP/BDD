from bddint_app.models import Utilisateur

def add_user(nom,prenom):
    user = Utilisateur(nom="John Doe", email="john@example.com")
    user.save()  # Sauvegarde dans la base de données