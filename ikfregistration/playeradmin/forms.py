from django import forms
from registration.models import Player,MasterCity,MasterState,MasterGroup,MasterSeason,MasterCategory,MasterRoles,MasterPosition
from uuid import uuid1
from enum import Enum
# 
class GenderEnum(Enum):
    Male = 'Male'
    Female = 'Female'

    
class PlayerForm(forms.ModelForm):
    
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'dob'}))
    playeruploadid = forms.UUIDField(initial=uuid1(), widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'playeruploadid'}), disabled=True)
    season = forms.ModelChoiceField(queryset=MasterSeason.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'id': 'season'}), initial=MasterSeason.objects.get(id='S03'))
    category = forms.ModelChoiceField(queryset=MasterCategory.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'id': 'category'}), initial=MasterCategory.objects.get(id='C'))
    whoisfilling = forms.ModelChoiceField(queryset=MasterRoles.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'id': 'whoisfilling'}), initial=MasterRoles.objects.get(id='Player'))
    gender = forms.ChoiceField(choices=[(gender.name, gender.value) for gender in GenderEnum])    

    class Meta:
        model = Player
        fields = ['tournament_state', 'tournament_city', 'first_name', 'last_name', 'primary_position', 'secondary_position', 'mobile', 'whatsapp', 'email','group','gender','dob','playeruploadid','season','category','whoisfilling']
        widgets = {
            'tournament_state': forms.Select(attrs={'class': 'form-control', 'id': 'tournament_state'}),
            'tournament_city': forms.Select(attrs={'class': 'form-control', 'id': 'tournament_city'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'last_name','required': False}),
            'primary_position': forms.Select(attrs={'class': 'form-control', 'id': 'primary_position'}),
            'secondary_position': forms.Select(attrs={'class': 'form-control', 'id': 'secondary_position'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'id': 'mobile'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'id': 'whatsapp'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email'}),
            'group': forms.Select(attrs={'class': 'form-control', 'id': 'group'}),
            
        }

        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = MasterGroup.objects.filter(include=True)
        self.fields['primary_position'].choices =  [(pos.id, f"{pos.id} . {pos.label}") for pos in MasterPosition.objects.all()]
        self.fields['secondary_position'].choices =  [(spos.id, f"{spos.id} . {spos.label}") for spos in MasterPosition.objects.all()]
        self.fields['tournament_state'].choices = [("", "--------")] + [(st.id, f"{st.id} . {st.name}") for st in MasterState.objects.all()]