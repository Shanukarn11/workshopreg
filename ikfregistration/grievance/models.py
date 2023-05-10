from django.db import models
from registration.models import MasterCity,MasterState,MasterPosition,MasterSeason,MasterRoles,MasterCategory,MasterGroup

# Create your models here.


class Grievance(models.Model):
    id = models.BigAutoField(primary_key=True)
    resolved = models.BooleanField(null=True,blank=True, default=False, db_index=True)
    description = models.TextField(null=True,blank=True)
    
    tournament_city = models.ForeignKey( 
        MasterCity, null=True, verbose_name="master city", db_index=True, on_delete=models.SET_NULL)
    tournament_state = models.ForeignKey(
        MasterState, null=True, verbose_name="master state", related_name='state2_gr', db_index=True, on_delete=models.SET_NULL)

#   profile
    gender = models.CharField(max_length=200, null=True, db_index=True)
    first_name = models.CharField(max_length=300, null=True)
    last_name = models.CharField(max_length=300, null=True,blank=True)

#   Player Position
    primary_position = models.ForeignKey(MasterPosition, null=True, related_name='primary_position2_gr',
                                         verbose_name="primary position_gr", db_index=True, on_delete=models.SET_NULL)
    secondary_position = models.ForeignKey(MasterPosition, null=True, related_name='secondary_position_gr',
                                           verbose_name="secondary position_gr", db_index=True, on_delete=models.SET_NULL)

#   Contact Information
    mobile = models.CharField(max_length=10, null=True, default="")

    whatsapp = models.CharField(max_length=10,blank=True, null=True)
    email = models.EmailField(null=True,blank=True,)
    screenshot = models.ImageField(upload_to='media/grievance/', blank=True, null=True)
 
 

#   Dates
    dob = models.DateField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    season = models.ForeignKey(
        MasterSeason, null=True, verbose_name="master_season_id", db_index=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(
        MasterCategory, null=True, verbose_name="master_category_id", db_index=True, on_delete=models.SET_NULL)

    whoisfilling = models.ForeignKey(
        MasterRoles, null=True, verbose_name="master_roles_id", db_index=True, on_delete=models.SET_NULL)
    whatsapp_sent = models.BooleanField(null=True,blank=True, default=False, db_index=True)

    player_added_interakt = models.BooleanField(null=True,blank=True, default=False, db_index=True)
    
    

    def __repr__(self) -> str:
        return str(self.first_name)

