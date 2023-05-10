from django.contrib import admin
from django.urls import path
from grievance import views
from django.conf.urls.static import static
from django.conf import settings
import re


urlpatterns = [
    path("", views.grievance, name='grievance'),
    ]