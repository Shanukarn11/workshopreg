#coding: utf8


import json
from django.core import serializers

from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse

from django.views.static import serve

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



from registration.modelhome import SocialMediaLink
from registration.models import MasterAmount, MasterCategory, MasterColumn, MasterDateLimit, MasterDocument, MasterGroup, MasterGroupCity, MasterLabels, MasterPartner, MasterRoles, MasterSeason, MasterState, MasterCity, MasterPosition, Player, Upload, Uploadfile,FailedPayment
from registration.forms import UploadForm, UploadfileForm

from django.db import IntegrityError
from django.db.models import Q
from django.views.decorators.cache import cache_control

import qrcode
from PIL import Image

from barcode.writer import ImageWriter
import barcode
import oss2

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
# def login(request):
#     if request.method == 'POST':
#         season = request.POST.getlist('season')[0]
#         datevalue=list(MasterDateLimit.objects.filter(season=season).values())

#         return JsonResponse(datevalue[0], safe=False)

def login(request):
    lang = "en"
    langqueryset = MasterLabels.objects.filter().values('keydata', lang)
    dict = {}
    for item in langqueryset:
        dict[item['keydata']] = item[lang]
    return render(request, 'login.html', dict)

def verifylogin(request):
    if request.method == 'POST':
        ikfuniqueid = request.POST.getlist('ikfuniqueid')[0]
        mobile = request.POST.getlist('mobile')[0]
        player=list(Player.objects.filter(ikfuniqueid=ikfuniqueid,mobile=mobile).values())
        if player:
            dictdata=dict()
            dictdata['error']="false"
            dictdata['login']="success"
            dictdata['ikfuniqueid']=player[0]['ikfuniqueid']
            return JsonResponse(dictdata,safe=False)
        else:
            dictdata=dict()
            dictdata['error']="false"
            dictdata['login']="failed"
            return JsonResponse(dictdata, safe=False)   
    else:
        dictdata=dict()
        dictdata['error']="true"
        dictdata['login']="failed"
        return JsonResponse(dictdata, safe=False) 

def playerdashboard(request):
    lang = "en"

    langqueryset = MasterLabels.objects.filter().values('keydata', lang)

    mycolumns = MasterColumn.objects.filter(includep2=1).values(
        'columnid', 'label_key', 'type', 'orderid')

    dict = {}

    for item in langqueryset:
        dict[item['keydata']] = item[lang]
    for item in mycolumns:
        item['label'] = dict[item['label_key']]
    dict['formikf'] = mycolumns
    dict['url_prev'] = "uploaddoc"
    dict['preview_type'] = "preview2"
    dict['url_next'] = "main"
    dict['button_text'] = "Submit"
    if is_ajax(request=request):
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            return JsonResponse({'message': "yes"})

    else:
        form = UploadForm()
        dict["uploadform"]=form
        return render(request, 'playerdashboard.html', dict)
    

def playerdatalogin(request):
    if request.method == 'POST':
        
        ikfid = request.POST.get('ikfuniqueid')
        playerdata = list(Player.objects.filter(ikfuniqueid=ikfid).values())
        
        
    return JsonResponse(playerdata[0], safe=False)



def editplayer(request):
   
    if request.method == 'POST':
        
        print("req is post")
        dictstr = request.POST.getlist('data')[0]
        dictdata=json.loads(dictstr)

        try:
            obj = Player.objects.get(
                ikfuniqueid=dictdata["ikfuniqueid"]

            )
            obj.first_name=dictdata["first_name"]
            obj.last_name=dictdata["last_name"]
            obj.primary_position_id=dictdata["primary_position"]
            obj.secondary_position_id=dictdata["secondary_position"]
            obj.upload_id_frgn=Upload.objects.filter(unique=obj.playeruploadid).last()
            if(dictdata["pic_file"]):
                obj.pic_file=dictdata["pic_file"]

            

            obj.save() 
            errordict = {"error": "false","message": "Updated Successfully", "ikfuniqueid": obj.ikfuniqueid ,"id":obj.id}
   
            return JsonResponse(errordict, safe=False)
        except Player.DoesNotExist:
            errordict = {"error": "true","message": "Player does not exist"}
            return Http404
            
    else:
        errordict = {"error": "true","message": "Request Error"}
        return Http404
   


