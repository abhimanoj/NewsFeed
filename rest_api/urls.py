from django.conf.urls import include, url
from django.contrib.auth.models import User
from django.urls import path
from rest_framework import routers, serializers, viewsets

from rest_api import views

from . import views
from .models import *
from .serializers import *

router = routers.DefaultRouter()
router.register(r'Domain', views.DomainTable, 'domain')
router.register(r'Person', views.PersonTable, 'person')
router.register(r'Tag', views.TagTable, 'tag')
router.register(r'Currency', views.CurrencyTable, 'currency') 
 
urlpatterns = [
    path('index', views.index, name='index'),
    path('', include(router.urls)),
]
