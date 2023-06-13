

# Create your views here.
from django.shortcuts import render, redirect,HttpResponse
import threading
from .forms import PlayerForm
from registration.models import MasterState,MasterCity,MasterPosition,MasterSeason,MasterCategory,MasterRoles,Player
from django.http import JsonResponse
import random
from uuid import uuid1
import requests
import json
def send_whatsapp_public_message(mobilenumber,firstname,lastname,obj):
    try:
            url = 'https://api.interakt.ai/v1/public/message/'
            api_key = 'aWZNYkJ4UWFBTG5nUTZZVHdDTndLQ0ViZTV4d1o4cHBiNGdGV1Joc01SNDo='
            print('mobilenumber')
            print(mobilenumber)
            headers = {
                'Authorization': f'Basic {api_key}',
                'Content-Type': 'application/json'
            }
            payload = {
                'countryCode': '+91',
                'phoneNumber': mobilenumber,
                'callbackData': 'Succesfully sent Message',
                'type': 'Template',
                'template': {
                    'name': 'workshopregistrationsuccess',
                    'languageCode': 'en',
                    'headerValues': [
                        
                    ],
                    'bodyValues': [
                        firstname,
                        obj.ikfuniqueid,
                        obj.mobile
                        
                    ]
                }
            }
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                if response.status_code >= 200 and response.status_code < 300:
                    # The request was successful, do something here
                    print("Public message API request was successful!")
                    obj.whatsapp_sent=True
                    obj.save()
                else:
                    # The request failed, handle the error here
                    print(f"Public message API request failed with status code {response.status_code}")
                    print(response.content)

            except Exception as e:
                print(e)
                return None
    except Exception as ex:
        print(ex)
        return None
    
def interakt_add_user(mobilenumber,firstname,lastname,obj):
    try:
            city=MasterCity.objects.get(id=obj.tournament_city_id).city
            state=MasterState.objects.get(id=obj.tournament_state_id).name
            primary_position=MasterPosition.objects.get(id=obj.primary_position_id).label
            secondary_position=MasterPosition.objects.get(id=obj.secondary_position_id).label
            
            url = 'https://api.interakt.ai/v1/public/track/users/'
            api_key = 'aWZNYkJ4UWFBTG5nUTZZVHdDTndLQ0ViZTV4d1o4cHBiNGdGV1Joc01SNDo='
            print('mobilenumber')
            print(mobilenumber)
            headers = {
                'Authorization': f'Basic {api_key}',
                'Content-Type': 'application/json'
            }
            payload = {
            "userId": obj.ikfuniqueid,
            "phoneNumber": mobilenumber,
            "countryCode": "+91",
            "traits": {

                "first_name": obj.first_name,
                "last_name":obj.last_name,
                "gender":obj.gender,
                "email": obj.email,
                
                "contact_number":obj.mobile,
                "primary_position": primary_position,
                "secondary_position":secondary_position,
                "city":city,
                "state":state

            },
            "tags": ["Workshop",city]
        }
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                if response.status_code >= 200 and response.status_code < 300:
                    # The request was successful, do something here
                    print("add track API request was successful!")
                    obj.player_added_interakt=True
                    obj.save()
                else:
                    # The request failed, handle the error here
                    print(f"Add track API request failed with status code {response.status_code}")
                    print(response.content)

            except Exception as e:
                print(e)
                return None
    except Exception as exept:
        print(exept)
        return None
def playerdetails(request):
    unique_id = uuid1()
    random_number = random.randint(100, 999)
    playerunique= str(unique_id) +str(random_number)
    

    if request.method == 'POST':
        try:
            form = PlayerForm(request.POST)
            if form.is_valid():
                player = form.save(commit=False)
                player.save()
                print(player)
                newplayerobj=Player.objects.get(id=player.id)
                try:

                   
                    city = MasterCity.objects.get(
                        id=newplayerobj.tournament_city_id).city[0:3].upper()

                    # category=MasterCategory.objects.get(id=obj.category).id
                    gender = newplayerobj.gender[0:1]
                    number = f'{newplayerobj.id:06}'
                    
                    newplayerobj.ikfuniqueid = "IKF" + "S3" + city + gender + number + newplayerobj.category.id
                    newplayerobj.save() 
                    print("testing the player after save")
                    print(player.mobile)
                    print("testing after player after save")
                    
               
                    mobilenumber=""
                    if((newplayerobj.whatsapp==None) or (newplayerobj.whatsapp=="") or  (newplayerobj.whatsapp=="NA") or newplayerobj.whatsapp=="undefined"):
                        mobilenumber=newplayerobj.mobile
                    else:
                        mobilenumber=newplayerobj.whatsapp

                    t1 = threading.Thread(target=send_whatsapp_public_message,args=(mobilenumber,newplayerobj.first_name,newplayerobj.last_name,newplayerobj))
                    
                    t2 = threading.Thread(target=interakt_add_user,args=(mobilenumber,newplayerobj.first_name,newplayerobj.last_name,newplayerobj))
                    t1.start()
                    t2.start()
                    t1.join()
                    t2.join()
                    
                
                                
                    
                except Exception as e:
                    errordict = {"error": "true",
                                "message": "Player does not exist"}
                    return HttpResponse(json.dumps(errordict))
                return render(request, 'success.html', {"hello":"success"})
                # return redirect('playeradmin:success')
        except Exception as e:
            form.add_error(None, f"An error occurred: {str(e)}")
    else:
        form = PlayerForm(initial={'playeruploadid': playerunique})
        return render(request, 'playeradmin.html', {'form': form})
