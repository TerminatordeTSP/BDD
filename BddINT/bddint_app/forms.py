from django import forms
from bddint_app.models import Camion, Chauffeur, Logins


class LoginForm(forms.Form):
    login = forms.CharField(max_length=255)
    mot_de_passe = forms.CharField(widget=forms.PasswordInput)


class CamionForm(forms.ModelForm):
    class Meta:
        model = Camion
        fields = '__all__'

class ChauffeurForm(forms.ModelForm):
    class Meta:
        model = Chauffeur
        fields = '__all__'

class RequetteForm(forms.Form):
    type_de_camion = forms.CharField(max_length=255)
    ville_d_arrivée = forms.CharField(max_length=255)

class LocalisationForm(forms.Form):
    type = forms.CharField(max_length=255)
    date = forms.DateField()