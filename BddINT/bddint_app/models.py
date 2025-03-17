from django.db import models

class Camion(models.Model):
    numéro_d_immatriculation = models.CharField(max_length=50, primary_key=True)
    type = models.CharField(max_length=50)
    poid_total_transportable_kg = models.DecimalField(max_digits=7, decimal_places=3)

    class Meta:
        db_table = 'Camion'  # Spécifie le nom de la table existante dans MySQL

    def __str__(self):
        return self.numéro_d_immatriculation

class Chauffeur(models.Model):
    numéro_de_permis_de_conduire = models.CharField(max_length=50, primary_key=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    class Meta:
        db_table = 'Chauffeur'  # Spécifie le nom de la table existante dans MySQL

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Marchandise(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    type_camion = models.CharField(max_length=50)
    poids = models.IntegerField()
    date_transport = models.DateField()
    ville_de_départ = models.CharField(max_length=50)
    ville_d_arrivee = models.CharField(max_length=50)
    camion = models.ForeignKey(Camion, on_delete=models.CASCADE)
    class Meta:
        db_table = 'Marchandise'  # Spécifie le nom de la table existante dans MySQL
    def __str__(self):
        return self.nom

class Affectation(models.Model):
    numéro_d_immatriculation = models.ForeignKey(Camion, on_delete=models.CASCADE, db_column='numéro_d_immatriculation')
    numéro_de_permis_de_conduire = models.ForeignKey(Chauffeur, on_delete=models.CASCADE,db_column='numéro_de_permis_de_conduire')
    date_affectation = models.DateField()
    class Meta:
        db_table = 'Affectation'  # Spécifie le nom de la table existante dans MySQL
        unique_together = ('numéro_d_immatriculation', 'numéro_de_permis_de_conduire') # la clé primaire est composée de ces 2 collones. Cela permet de garantir qu’il n’y a pas de doublons pour cette combinaison spécifique.

    def __str__(self):
        return f"{self.numéro_d_immatriculation} - {self.numéro_de_permis_de_conduire}"

class Logins(models.Model):
    login = models.CharField(max_length=50, primary_key=True)
    mot_de_passe = models.CharField(max_length=50)
    role = models.CharField(max_length=50, null=True, blank=True)
    class Meta:
        db_table = 'Logins'  # Spécifie le nom de la table existante dans MySQL
    def __str__(self):
        return self.login