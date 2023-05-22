#coding: utf8
import os
import requests
import threading
import random
import shutil
import json
import glob
import subprocess
import time
from uuid import uuid1
import PIL
from django.core import serializers
from django.utils.html import escape
import razorpay
import datetime
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse

from django.views.static import serve

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

import pathlib
from django.db import transaction

from registration.modelhome import SocialMediaLink
from .models import MasterAmount, MasterCategory, MasterColumn, MasterDateLimit, MasterDocument, MasterGroup, MasterGroupCity, MasterLabels, MasterPartner, MasterRoles, MasterSeason, MasterState, MasterCity, MasterPosition, Player, Upload, Uploadfile,FailedPayment,ScoutCourse,ScoutCourseDiscount,ScoutDiscountType,SelectionStatus,HomeBanner,WorkShopsReg_Images,WorkShopsRegButton,WorkShopsRegExperts,WorkShopsRegFeatureStrip,TabelWorkshopsReg,ActiveStatusNav,TrialsAndInitiativeNav,Previous_Workshop_Images,Winners_Workshop_Images,Testimonials
from .forms import UploadForm, UploadfileForm

from django.db import IntegrityError
from django.views.decorators.cache import cache_control

import qrcode
from PIL import Image

from barcode.writer import ImageWriter
import barcode
import oss2
import asyncio
from dotenv import load_dotenv
load_dotenv()
OSS_ACCESS_KEY_ID = "LTAI5tJoy1BhmrzS6vWDM73F"
OSS_ACCESS_KEY_SECRET = "WUEAB6baG5LI17dLy3vkGfAi9pVwlS"
OSS_BUCKET_NAME = "ikfseason2"
OSS_BUCKET_ACL = "public-read"  # private, public-read, public-read-write

# # Refer https://www.alibabacloud.com/help/zh/doc-detail/31837.htm about endpoint
OSS_ENDPOINT = "oss-ap-south-1.aliyuncs.com"

def amount(request):
    if request.method == "POST":
        datastr = request.POST.getlist('data')[0]
        data = json.loads(datastr)
        print(data['tournament_city'])
        print(data['season'])
        print(data['group'])
        print(data['whoisfilling'])
        #printdata['tournament_city'])
        try:
                amount = MasterAmount.objects.filter(
                    city_id=data['tournament_city'],
                    season=data['season'],
                    group=data['group'],
                    coach_or_player=data["whoisfilling"]).values()
                print(amount[0]["amount"])
                
                amount_value=amount[0]["amount"]
                return HttpResponse(amount_value)
        except Exception as e:
            print(e)
            return Http404
 
        


def order(request):
    if request.method == "POST":
        
        unique_id = uuid1()
        
        mobile= request.POST.getlist('mobile')[0]
        random_number = random.randint(100, 999)
        
        playerunique= str(unique_id) +str(random_number)


        amountinput=int(request.POST.getlist('amount')[0])
        amount = amountinput*100
 

        client = razorpay.Client(
            auth=(os.environ.get('RAZORPAY_KEY_ID'), os.environ.get('RAZORPAY_KEY_SECRET')))
        DATA = {
            "amount": amount,
            "currency": "INR",
            "receipt": playerunique,
            "notes": {"id": playerunique, "mobile": mobile
                      }}
        response = client.order.create(data=DATA)
        return HttpResponse(json.dumps({"order_id":response["id"], "ikfplayerunique":playerunique}))



@cache_control(no_cache=True, must_revalidate=True)
def paymentfun(request):
    lang = "en"
    langqueryset = MasterLabels.objects.filter().values('keydata', lang)
    dict = {}
    for item in langqueryset:
        dict[item['keydata']] = item[lang]
    dict["RAZORPAY_KEY_ID"]=os.environ.get('RAZORPAY_KEY_ID')
    return render(request, 'player/payment.html', dict)

# with transaction.atomic():
#     for i, row in df.iterrows():
#         mv = MeasureValue.objects.get(org=row.org, month=month)

#         if (row.percentile is None) or np.isnan(row.percentile):
#             # if it's already None, why set it to None?
#             row.percentile = None

#         mv.percentile = row.percentile
#         mv.save()
# @transaction.atomic
# def viewfunc(request):
#     create_parent()

#     try:
#         with transaction.atomic():
#             generate_relationships()
#     except IntegrityError:
#         handle_exception()


#     add_children()
BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()
HOME_PATH = os.path.join(BASE_DIR, 'home')
STATIC_PATH = os.path.join(BASE_DIR, 'static')
CONFIG_FILE = 'config_win.json'

def pagelabel(lang):

    langqueryset = list(MasterLabels.objects.filter(
        ).values('keydata', lang))
    dictvalue = dict()
    for item in langqueryset:
        dictvalue[item['keydata']] = item[lang]
    return dictvalue
def homeindex(request):
    lang = "en"
    # langqueryset = MasterLabels.objects.filter().values('keydata', lang)
    
    # dict = {

    # }
    # socialMediaLink = SocialMediaLink.objects.filter(
    #     include=1, type_of_link="social").values('icon', 'url', 'name',)
    # website = SocialMediaLink.objects.filter(
    #     include=1, type_of_link="website").values('icon', 'url', 'name',)
    # phone = SocialMediaLink.objects.filter(
    #     include=1, type_of_link="phone").values('icon', 'url', 'name',)

    # # for notice board
    # # noticeBoard = NoticeBoard.objects.filter(include=1).values(
    # #     'title', 'description', 'isHeading', 'include',)
    # for item in langqueryset:
    #     dict[item['keydata']] = item[lang]

    # dict['social_links'] = socialMediaLink
    # dict['website_links'] = website
    # dict['phone_links'] = phone
    # dict['notice_board'] = ""
    # #printnoticeBoard)
    context = pagelabel(lang)
    workshopsRegimages = WorkShopsReg_Images.objects.filter(lang=lang).values()

    dictvar = dict()
    for img in workshopsRegimages:
        dictvar[img['keydata']] = img['pic']
    

    context['banners'] = HomeBanner.objects.filter(lang=lang).values()
    context['WorkshopsRegTabel'] = TabelWorkshopsReg.objects.filter(
        lang=lang).values()
    context['buttonsReg'] = WorkShopsRegButton.objects.filter(
        lang=lang).values()
    context['featurestripsReg'] = WorkShopsRegFeatureStrip.objects.filter(
        lang=lang).values()
    context['learnfromexpertsReg'] = WorkShopsRegExperts.objects.filter(
        lang=lang).values()
    context['previous_workshop'] = Previous_Workshop_Images.objects.filter(
        lang=lang).values()
    context['winners_workshop'] = Winners_Workshop_Images.objects.filter(
        lang=lang).values()
    context['testimonials'] = Testimonials.objects.filter(
        lang=lang).values()
    context['workshopsRegimages'] = dictvar
    context['TrialsAndInitiativeNav'] = TrialsAndInitiativeNav.objects.filter(pagetype="workshopsreg",
                                                                              lang=lang).values()

    
    context['code']=request.GET.get('code')
    return render(request, 'index.html', context)


def category(request, lang):

    langqueryset = MasterLabels.objects.filter().values('keydata', lang)
    dict = {}
    for item in langqueryset:
        dict[item['keydata']] = item[lang]
    masterroles = MasterRoles.objects.filter(include=1).values()
    dict['masterroles'] = masterroles

    return render(request, 'category.html', dict)


def coachorplayer(request, lang, category):
    context = {}

    langqueryset = MasterLabels.objects.filter().values('keydata', lang)
    dict = {}

    for item in langqueryset:
        dict[item['keydata']] = item[lang]
    if(category == "Coach"):
        dict["coach_or_player"] = "Coach"
        return redirect('/coach/', dict)

    else:
        dict["coach_or_player"] = "Player"
        return render(request, 'player/player.html', dict)


def main(request):
    context = {}
    lang = "en"
    langqueryset = MasterLabels.objects.filter().values('keydata', lang)
    dict = {}
    for item in langqueryset:
        dict[item['keydata']] = item[lang]
    #printuuid1())
    uniqueid=uuid1()
    random_number = random.randint(100, 999)
    dict['playeruploadid'] = str(uniqueid) +str(random_number)
    
    if is_ajax(request=request):
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            return JsonResponse({'message': "yes"})

    else:
        form = UploadForm()
        dict["uploadform"]=form
        return render(request, 'player/main.html', dict)


def preview1(request):

    lang = "en"
    langqueryset = MasterLabels.objects.filter().values('keydata', lang)

    mycolumns = MasterColumn.objects.filter(includep1=1).values(
        'columnid', 'label_key', 'type', 'orderid')
    dict = {

    }

    for item in langqueryset:
        dict[item['keydata']] = item[lang]
    arrayfordict = []

    for item in mycolumns:
        item['label'] = dict[item['label_key']]

    dict['formikf'] = mycolumns

    dict['preview_type'] = "preview1"
    dict['url_prev'] = "coachorplayer"
    dict['url_prev_para'] = "Player"
    dict['url_next'] = "main"
    dict['button_text'] = "Next"

    return render(request, 'player/preview.html', dict)


@cache_control(no_cache=True, must_revalidate=True)
def preview2(request):

    #
    imageid = "d83f5a87-dfdb-11ec-a390-b42e990d79d6"
    lang = "en"
    langqueryset = MasterLabels.objects.filter().values('keydata', lang)

    mycolumns = MasterColumn.objects.filter(includep2=1).values(
        'columnid', 'label_key', 'type', 'orderid')

    dict = {

    }

    for item in langqueryset:
        dict[item['keydata']] = item[lang]
    for item in mycolumns:
        item['label'] = dict[item['label_key']]
    dict['formikf'] = mycolumns
    dict['url_prev'] = "uploaddoc"
    dict['preview_type'] = "preview2"
    dict['url_next'] = "main"
    dict['button_text'] = "Save"


    return render(request, 'player/preview.html', dict)

def viewpic(request):
    dict={}
    if request.method=="POST":
        
        
        imageid = request.POST.getlist('playeruploadidfinal')[0]
        
        if(imageid):
            print("Image id")
            print(imageid)
            myupload = Upload.objects.filter(unique=imageid).last()
            dict['myupload']=myupload
            image_url = myupload.image.url + '?v=' + escape(str(myupload.id))
            #printmyupload.image.url)
            return HttpResponse(image_url)

        else:
            dict['myupload'] = ""
            return HttpResponse("")
            
    else:
        dict['myupload'] = ""
        return HttpResponse("")
        
def viewdoc(request):
    dict={}
    if request.method=="POST":
        
        
        imageid = request.POST.getlist('playeruploadidfinal')[0]
        if(imageid):
            myupload = Uploadfile.objects.filter(unique=imageid).last()
            dict['myupload']=myupload
            
            return HttpResponse(myupload.file.url)

        else:
            dict['myupload'] = ""
            return HttpResponse("")
            
    else:
        dict['myupload'] = ""
        return HttpResponse("")


def viewdocpic(request):
    dict={}
    if request.method=="POST":
        
        
        imageid = request.POST.getlist('playeruploadidfinal')[0]
        if(imageid):
            myupload = Upload.objects.filter(unique=imageid).order_by("-id")[0]
            myuploadfile = Uploadfile.objects.filter(unique=imageid).order_by("-id")[0]
            if(myupload and myuploadfile):
                dict['pic']=myupload.image.url
                dict['doc']=myuploadfile.file.url
                return JsonResponse(dict)
            elif(myupload):
                dict['pic']=myupload.image.url
                dict['doc']=""
                return JsonResponse(dict)
            elif(myuploadfile):
                dict['pic']=""
                dict['doc']=myuploadfile.file.url
                return JsonResponse(dict)
            else:
                return JsonResponse({})



        else:
            dict['myupload'] = ""
            return JsonResponse({})
            
    else:
        dict['myupload'] = ""
        return HttpResponse("")

def printpdf(request):
    if request.method=="GET":
        context = {}
        lang = "en"
        langqueryset = MasterLabels.objects.filter().values('keydata', lang)
        dict = {}
        for item in langqueryset:
            dict[item['keydata']] = item[lang]
        return render(request, 'player/printpdf.html', dict)
def paymentfail(request):
    if request.method=="GET":
        context = {}
        lang = "en"
        langqueryset = MasterLabels.objects.filter().values('keydata', lang)
        dict = {}
        for item in langqueryset:
            dict[item['keydata']] = item[lang]
        return render(request, 'player/paymentfail.html', dict)    

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def handle_uploaded_file(f):
    print(f.name)
    
    auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET_NAME)
    headers=dict()
    # headers["x-oss-storage-class"] = "Standard"
    # headers["x-oss-object-acl"] = oss2.OBJECT_ACL_PUBLIC_READ
    # headers['x-oss-process']="image/resize,w_300,h_300"
    headers['x-oss-forbid-overwrite']="false"
    f.seek(1000, os.SEEK_SET)
    filename="images/" +f.name
    result=bucket.put_object(filename,f,headers=headers)
    print(result)
    # f.seek(1000, os.SEEK_SET)
    # current = f.tell()
    # for chunk in f.chunks():
    #     result= 
    #     print(result)   
     
    
    
# with open('D:\\localpath\\examplefile.txt', 'rb') as fileobj:
#     # Use the seek method to read data from byte 1000 of the file. The data is uploaded from byte 1000 to the last byte of the local file. 
    # f.seek(1000, os.SEEK_SET)
    # # Use the tell method to obtain the current position. 
    # current = f.tell()
#     print(auth)
    # with open(f, 'wb+') as destination:
    #     for chunk in f.chunks():
    #         destination.write(chunk)
def uploaddoc(request):
    lang = "en"
    langqueryset = MasterLabels.objects.filter().values('keydata', lang)
    dict = {}
    for item in langqueryset:
        dict[item['keydata']] = item[lang]

    if is_ajax(request=request):
        form = UploadfileForm(request.POST, request.FILES)

        if form.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            form.save()

            return JsonResponse({'message': "yes"})

    else:
        form = UploadfileForm()
        dict["uploadfileform"] = form
        return render(request, 'player/uploaddoc.html', dict)


def uploadpic(request):
    lang = "en"
    langqueryset = MasterLabels.objects.filter().values('keydata', lang)
    dict = {}
    for item in langqueryset:
        dict[item['keydata']] = item[lang]

    if is_ajax(request=request):
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():

            form.save()

            return JsonResponse({'message': "yes"})

    else:
        form = UploadForm()
        dict["uploadform"]=form
        return render(request, 'player/uploadpic.html', dict)






def statedata(request):
    if request.method == 'POST':
        #      try:

        #     F.objects.filter().update(status='P')
        #     F.objects.filter(file=filename).update(status='C')
        include = request.POST.getlist('include')[0]
        if(include == "3" or include == 3):
            state = MasterState.objects.filter()
        else:
            state = MasterState.objects.filter(include=include)
        statevalue = state.values()
        #printstatevalue)
        arrayobj = []

        for state in statevalue:
            newstate = {}
            newstate['value'] = state['name']
            newstate['id'] = state['id']
            arrayobj.append(newstate)
        
        js_state = json.dumps(arrayobj)
        return HttpResponse(js_state)

    #           # If get() throws an error you need to handle it.
    #           # You can use either the generic ObjectDoesNotExist or
    #           # <model>.DoesNotExist which inherits from
    #           # django.core.exceptions.ObjectDoesNotExist, so you can target multiple
    #           # DoesNotExist exceptions
    #      except MasterState.DoesNotExist: # or the generic "except ObjectDoesNotExist:"
    #            #print"State Does Not Exist")
    #            return HttpResponse({})


def citydata(request):
    if request.method == 'POST':
        
        #printstate)
    #      try:

    #     F.objects.filter().update(status='P')
    #     F.objects.filter(file=filename).update(status='C')
        city = MasterCity.objects.filter(include=1)
        cityvalue = city.values()

        arrayobj = []

        for cityitem in cityvalue:
            newcity = {}
            newcity['value'] = cityitem['city']
            newcity['id'] = cityitem['id']
            arrayobj.append(newcity)

        js_city = json.dumps(arrayobj)
        return HttpResponse(js_city)

    #           # If get() throws an error you need to handle it.
    #           # You can use either the generic ObjectDoesNotExist or
    #           # <model>.DoesNotExist which inherits from
    #           # django.core.exceptions.ObjectDoesNotExist, so you can target multiple
    #           # DoesNotExist exceptions
    #      except MasterState.DoesNotExist: # or the generic "except ObjectDoesNotExist:"
    #            #print"State Does Not Exist")
    #            return HttpResponse({})


def positiondata(request):
    if request.method == 'POST':

        positions = MasterPosition.objects.filter()
        positionvalue = positions.values()
        #printpositionvalue)
        arrayobj = []

        for position in positionvalue:
            newstate = {}
            newstate['value'] = position['label']
            newstate['id'] = position['id']
            arrayobj.append(newstate)

        js_state = json.dumps(arrayobj)
        return HttpResponse(js_state)


def documentdata(request):
    if request.method == 'POST':

        positions = MasterDocument.objects.filter(include=1)
        positionvalue = positions.values()
        #printpositionvalue)
        arrayobj = []
        lang = 'en'
        for position in positionvalue:
            newstate = {}
            newstate['value'] = position[lang]
            newstate['id'] = position['id']
            arrayobj.append(newstate)

        js_state = json.dumps(arrayobj)
        return HttpResponse(js_state)



def send_whatsapp_public_message(mobilenumber,firstname,lastname,obj):
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
            'name': 'registration',
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
    
def interakt_add_user(mobilenumber,firstname,lastname,obj):
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
    "tags": ["S3",city]
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
    
def save(request):
    if request.method == 'POST':
        datastr = request.POST.getlist('data')[0]
        extrafield1=request.POST.getlist('extrafield1')[0]
        dictdata = json.loads(datastr)


        context = {}

            


        player = Player(
            tournament_city=MasterCity.objects.get(
                id=dictdata['tournament_city']),

            gender=dictdata['gender'],
            first_name=dictdata['first_name'],
            last_name=dictdata['last_name'],

            primary_position=MasterPosition.objects.get(
                id=dictdata['primary_position']),
            secondary_position=MasterPosition.objects.get(
                id=dictdata['secondary_position']),
            mobile=dictdata['mobile'],
            radiomobile=dictdata['radiomobile'],
            whatsapp=dictdata['whatsapp'],
            email=dictdata['email'],
            dob=dictdata['dob'],
             status=request.POST.getlist('status')[0],
             razorpay_unique_id=request.POST.getlist('razorpay_unique_id')[0],
             razorpay_payment_id=request.POST.getlist('razorpay_payment_id')[0],
             razorpay_order_id=request.POST.getlist('razorpay_order_id')[0],
             razorpay_signature=request.POST.getlist('razorpay_signature')[0],


             amount=request.POST.getlist('amount')[0],

            playeruploadid=dictdata['playeruploadid'],
     
            pic_file=dictdata['pic_file'],


            group=MasterGroup.objects.get(id=dictdata['group']),
            season=MasterSeason.objects.get(id=dictdata['season']),
            category=MasterCategory.objects.get(id=dictdata['category']),
            whoisfilling=MasterRoles.objects.get(id=dictdata['whoisfilling']),
            upload_id_frgn=Upload.objects.filter(unique=dictdata['playeruploadid']).last(),
            referral = dictdata['referral'],
            discount = dictdata['discount'],
            extrafield1=extrafield1,
        )

        try:
            player.save()
            try:
                obj = Player.objects.get(
                    tournament_city=MasterCity.objects.get(
                        id=dictdata['tournament_city']),

        

                    playeruploadid=dictdata['playeruploadid'],
                    dob=dictdata['dob'],
                    mobile=dictdata['mobile'],

                )

                city = MasterCity.objects.get(
                    id=obj.tournament_city_id).city[0:3].upper()

                # category=MasterCategory.objects.get(id=obj.category).id
                gender = obj.gender[0:1]
                number = f'{obj.id:06}'

                obj.ikfuniqueid = "IKF" + "S3" +  city + gender + number + obj.category.id
                obj.save() 
                errordict = {"error": "false",
                             "message": "Saved Successfully", "ikfuniqueid": obj.ikfuniqueid ,"id":obj.id}
                mobilenumber=""
                if((obj.whatsapp==None) or (obj.whatsapp=="") or  (obj.whatsapp=="NA") or obj.whatsapp=="undefined"):
                    mobilenumber=obj.mobile
                else:
                    mobilenumber=obj.whatsapp

                t1 = threading.Thread(target=send_whatsapp_public_message,args=(mobilenumber,obj.first_name,obj.last_name,obj))
                
                t2 = threading.Thread(target=interakt_add_user,args=(mobilenumber,obj.first_name,obj.last_name,obj))
                t1.start()
                t2.start()
                t1.join()
                t2.join()
               
                             
                return HttpResponse(json.dumps(errordict))
            except Player.DoesNotExist:
                errordict = {"error": "true",
                             "message": "Player does not exist"}
                return HttpResponse(json.dumps(errordict))

        except IntegrityError as e:
            #printe)

            errordict = {"error": "true", "message": str(e)}
            #printjson.dumps(errordict))
            return HttpResponse(json.dumps(errordict))


def converter(request):
    if request.method == 'POST':
        inputid = request.POST.getlist('id')[0]
        if(inputid=="" or inputid=="undefined" or inputid=="NA"):
            inputid=None
        inputtype = request.POST.getlist('type')[0]
        if(inputtype == "state" or inputtype == "state_id" or  inputtype == "tournament_state" or inputtype == "tournament_state_id"):
            input = MasterState.objects.filter(id=inputid)
            namevar = 'name'
            inputvalue = input.values()
            arrayobj = []

            for inpu in inputvalue:
                output = {}
                output['label'] = inpu[namevar]

                arrayobj.append(output)
            js_state = json.dumps(arrayobj)
            return HttpResponse(js_state)

        elif(inputtype == "tournament_city" or inputtype == "tournament_city_id"):
            input = MasterCity.objects.filter(id=inputid)
            namevar = 'city'
            inputvalue = input.values()
            arrayobj = []

            for inpu in inputvalue:
                output = {}
                output['label'] = inpu[namevar]

                arrayobj.append(output)
            js_state = json.dumps(arrayobj)
            return HttpResponse(js_state)
        elif(inputtype == "primary_position" or inputtype == "primary_position_id" or inputtype == "secondary_position" or inputtype == "secondary_position_id"):
            input = MasterPosition.objects.filter(id=inputid)
            namevar = 'label'
            inputvalue = input.values()

            arrayobj = []

            for inpu in inputvalue:
                output = {}
                output['label'] = inpu[namevar]

                arrayobj.append(output)
            js_state = json.dumps(arrayobj)
            return HttpResponse(js_state)
        elif(inputtype == "document_id_selected_id" or inputtype=="document_id_selected"):
            #print'document input id',inputid)
            input = MasterDocument.objects.filter(id=inputid)
            lang = "en"
            namevar = lang
            inputvalue = input.values()
            arrayobj = []

            for inpu in inputvalue:
                output = {}
                output['label'] = inpu[namevar]

                arrayobj.append(output)
            js_state = json.dumps(arrayobj)
            return HttpResponse(js_state)


def mygroup(request):
    if request.method == 'POST':
        gender = request.POST.getlist('gender')[0]
        dob = request.POST.getlist('dob')[0]
        city = request.POST.getlist('city')[0]
        #printdob)
        # datedob=datetime.datetime(dob)
        include = request.POST.getlist('include')[0]

        datagroup = MasterGroup.objects.filter(
            gender=gender, include=include, start__lte=dob, end__gte=dob).values()
        if(datagroup):
            #print"group id :")
            #printdatagroup[0]['id'])
            #print"city id")
            #printcity)
            datacity = MasterGroupCity.objects.filter(
                cityid_id=city, groupid_id=datagroup[0]['id']).values()
            #printdatacity)
            if(datacity):
                context = {
                    "present": "1",
                    "id": datagroup[0]['id'],
                    "group": datagroup[0]['group'],

                    "gender": datagroup[0]['gender'],
                    "start": datagroup[0]['start'].strftime("%d %b %Y "),
                    "end": datagroup[0]['end'].strftime("%d %b %Y ")
                }
                js_state = json.dumps(context)
                return HttpResponse(js_state)
            else:
                context = {
                    "present": "0",
                    "text_code": "error_code"
                }

                js_state = json.dumps(context)
                return HttpResponse(js_state)
        else:
            context = {
                "present": "0",
                "text_code": "error_code"
            }
            js_state = json.dumps(context)
            return HttpResponse(js_state)


# FOR PLAYER DATA IN PRINT PDF

def playerdata(request):
    if request.method == 'POST':
        
        ikfid = request.POST.get('ikfuniqueid')
        playerdata = list(Player.objects.filter(ikfuniqueid=ikfid).values())
        print(playerdata)
        generatebarcode(playerdata[0])
    return JsonResponse(playerdata[0], safe=False)

# For partner info

def partnerinfo(request):
    if request.method == 'POST':
        season = request.POST.get('season')
        city = request.POST.get('city')
        category = request.POST.get('category')
        partnerdata = list(MasterPartner.objects.filter(season=season,city=city,category=category).values())
        
        print(partnerdata)
    return JsonResponse(partnerdata[0], safe=False)

# To generate QR

def generateqrcode(data):
    # taking base width
    basewidth = 100
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    
    # url = 'https://www.geeksforgeeks.org/'
    
    # adding URL or text to QRcode
    QRcode.add_data(data)
    
    # generating QR code
    QRcode.make()
    QRcolor = 'Green'
    
    # adding color to QR code
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color="white").convert('RGB')
    QRimg.save(data[0]['playeruploadid']+'.png')
    
    #print'QR code generated!')


def generatebarcode(data):
    ikfuniqueid = data['ikfuniqueid']
    modifiedid=ikfuniqueid.replace("-","")
    hr= barcode.get_barcode_class('code128')
    Hr=hr(str(modifiedid), writer=ImageWriter())
    Hr.save('media/barcode/'+ikfuniqueid)
    to_be_resized = Image.open('media/barcode/'+ikfuniqueid+'.png')
    newSize = (270, 90)
    resized = to_be_resized.resize(newSize, resample=PIL.Image.NEAREST) 
    print(resized)
    resized.save('media/barcode/'+ikfuniqueid+'.png')

def paymentstatus(request):
    if request.method == 'POST':
            razorpay_unique_id = request.POST.getlist('razorpay_unique_id')[0]
            playeruploadid=request.POST.getlist('playeruploadid')[0]

            payment=FailedPayment(
             razorpay_unique_id=razorpay_unique_id,
             playeruploadid=playeruploadid,
             status=request.POST.getlist('status')[0],
             razorpay_payment_id=request.POST.getlist('razorpay_payment_id')[0],
             razorpay_order_id=request.POST.getlist('razorpay_order_id')[0],
             razorpay_signature=request.POST.getlist('razorpay_signature')[0],

             error_code=request.POST.getlist('error_code')[0],
             error_description=request.POST.getlist('error_description')[0],
             error_source=request.POST.getlist('error_source')[0],
             error_reason=request.POST.getlist('error_reason')[0],
             error_meta_order_id=request.POST.getlist('error_meta_order_id')[0],
             error_meta_payment_id=request.POST.getlist('error_meta_payment_id')[0],
             amount=request.POST.getlist('amount')[0]

          
            )
            payment.save()
            errordict = {"error": "false",
                            "message": "Failded Payment Saved Successfully"}
            return HttpResponse(json.dumps(errordict))



def limitdate(request):
    if request.method == 'POST':
        season = request.POST.getlist('season')[0]
        datevalue=list(MasterDateLimit.objects.filter(season=season).values())
        return JsonResponse(datevalue[0], safe=False)
    
def successpayment(request):
    context = {}
    lang = "en"
    langqueryset = MasterLabels.objects.filter().values('keydata', lang)
    dict = {}
    for item in langqueryset:
        dict[item['keydata']] = item[lang]

    return render(request, 'player/successpayment.html', dict)

def scoutdiscountamount(request):
    if request.method == 'POST':
        typeofdiscount = request.POST.getlist('type')[0]
        course = request.POST.getlist('course')[0]
        courseamount=list(ScoutCourse.objects.filter(id=course ).values())
        if (typeofdiscount == None or typeofdiscount == ""):
            newdict={}
            newdict['amount']=float(courseamount[0]['amount'])
            return JsonResponse(newdict, safe=False)
        else:
            scoutamount=list(ScoutCourseDiscount.objects.filter(type=typeofdiscount,course=course ).values())
            print(float(scoutamount[0]['discount']))
            print(float(courseamount[0]['amount']))
            newdict={}
            newdict['amount']=float(courseamount[0]['amount']) -float(scoutamount[0]['discount'])
            return JsonResponse(newdict, safe=False)
