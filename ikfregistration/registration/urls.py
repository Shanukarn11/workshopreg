#coding: utf8
from django.contrib import admin
from django.urls import path
from registration import views
from django.conf.urls.static import static
from django.conf import settings
import re


urlpatterns = [
    path("", views.homeindex, name='homeindex'),
    path("category/<lang>", views.category, name='category'),
    path("coachorplayer/<lang>/<category>",
         views.coachorplayer, name='coachorplayer'),



    path("main", views.main, name='main'),
    path("mygroup", views.mygroup, name='mygroup'),
    path("preview1", views.preview1, name='preview1'),
    path("preview2", views.preview2, name='preview2'),
    path("uploaddoc", views.uploaddoc, name='uploaddoc'),
    path("viewpic", views.viewpic, name='viewpic'),
    path("uploadpic", views.uploadpic, name='uploadpic'),
    path("viewdoc", views.viewdoc, name='viewdoc'),
    path("viewdocpic", views.viewdocpic, name='viewdocpic'),
    path("save", views.save, name='save'),
    path("update", views.update, name='update'),
    path("updatepaykey", views.updatepaykey, name='updatepaykey'),
    path("amount", views.amount, name="amount"),
    path("order", views.order, name='order'),
    path("phonepe", views.phonepe, name='phonepe'),
    path("orderphonepe", views.orderphonepe, name='orderphonepe'),
    path("phonepestatus", views.phonepestatus, name='phonepestatus'),
    
    path("payment", views.paymentfun, name='payment'),

    path("statedata", views.statedata, name='statedata'),
    path("citydata", views.citydata, name='citydata'),
    path("positiondata", views.positiondata, name='positiondata'),
    path("documentdata", views.documentdata, name='documentdata'),

    path("printpdf", views.printpdf, name='printpdf'),
    path("paymentfail", views.paymentfail, name='paymentfail'),

    path("converter", views.converter, name='converter'),

    path("playerdata",views.playerdata, name='playerdata'),
    path("partnerinfo",views.partnerinfo, name='partnerinfo'),
    path("paymentstatus",views.paymentstatus, name='paymentstatus'),
    

    path("limitdate",views.limitdate, name='limitdate'),
    path("successpayment",views.successpayment, name='successpayment'),
    path("scoutdiscountamount",views.scoutdiscountamount, name='scoutdiscountamount'),
    path("winnerinfo",views.winnerinfo, name='winnerinfo'),
    path("clubinfo",views.clubinfo, name='clubinfo'),
    path("faq",views.faq, name='faq'),
    path("refund",views.refund, name='refund'),
    path("term",views.term, name='term'),
    path('callback_handler/', views.callback_handler, name='callback_handler'),










]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
