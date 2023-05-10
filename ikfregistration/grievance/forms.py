from django import forms
from registration.models import MasterCity,MasterState,MasterGroup,MasterSeason,MasterCategory,MasterRoles,MasterPosition
from uuid import uuid1
from playeradmin.forms import GenderEnum
from grievance.models import Grievance
# 


    
class GrievanceForm(forms.ModelForm):
    
    screenshot = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control col-md-6-file', 'id': 'screenshot'}), required=False)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'dob'}))
    playeruploadid = forms.UUIDField(initial=uuid1(), widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'playeruploadid'}), disabled=True)
    season = forms.ModelChoiceField(queryset=MasterSeason.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'id': 'season'}), initial=MasterSeason.objects.get(id='S03'))
    category = forms.ModelChoiceField(queryset=MasterCategory.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'id': 'category'}), initial=MasterCategory.objects.get(id='C'))
    whoisfilling = forms.ModelChoiceField(queryset=MasterRoles.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'id': 'whoisfilling'}), initial=MasterRoles.objects.get(id='Player'))
    gender = forms.ChoiceField(choices=[(gender.name, gender.value) for gender in GenderEnum])   
    class Meta:
        model = Grievance
        fields = [ 'tournament_state', 'tournament_city', 
                  'gender', 'first_name', 'last_name', 'primary_position', 'secondary_position',
                  'mobile', 'whatsapp', 'email', 'screenshot', 'dob', 'description','resolved', 'season', 'category',
                  'whoisfilling', 'whatsapp_sent', 'player_added_interakt']


        widgets = {
            'tournament_city': forms.Select(attrs={'class': 'form-control col-md-6', 'id': 'tournament_city'}),
            'tournament_state': forms.Select(attrs={'class': 'form-control col-md-6', 'id': 'tournament_state'}),
           
            'first_name': forms.TextInput(attrs={'class': 'form-control col-md-6', 'id': 'first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control col-md-6', 'id': 'last_name'}),
            'primary_position': forms.Select(attrs={'class': 'form-control col-md-6', 'id': 'primary_position'}),
            'secondary_position': forms.Select(attrs={'class': 'form-control col-md-6', 'id': 'secondary_position'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control col-md-6', 'id': 'mobile'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control col-md-6', 'id': 'whatsapp'}),
            'email': forms.EmailInput(attrs={'class': 'form-control col-md-6', 'id': 'email'}),
            'dob': forms.DateInput(attrs={'class': 'form-control col-md-6', 'id': 'dob'}),
            'season': forms.Select(attrs={'class': 'form-control col-md-6', 'id': 'season'}),
            'category': forms.Select(attrs={'class': 'form-control col-md-6', 'id': 'category'}),
            'whoisfilling': forms.Select(attrs={'class': 'form-control col-md-6', 'id': 'whoisfilling'}),
        }
