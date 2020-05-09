from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, generics, permissions, renderers, response, schemas, viewsets)
from rest_framework.decorators import api_view, detail_route, renderer_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

from rest_api.models import *
from rest_api.permissions import IsOwnerOrReadOnly
from rest_api.serializers import *

from rest_framework.filters import OrderingFilter, SearchFilter


@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Mock Pooler IT markplace backend')
    return response.Response(generator.get_schema(request=request))

def index(request):
    return HttpResponse("Mock Pooler IT markplace backend")


#[Start] Override one of the pagination classes, and seting the attributes..
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

#[end]


 
    

class PersonTable(viewsets.ModelViewSet):
    """
    You can performe filter based on price field.
    """
    queryset = PersonTable.objects.all()
    serializer_class = PersonTableSerializer

    #Apply Filter..
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    
    filterset_fields = ['name']
    #Apply Sorting..
    ordering_fields = ['name']
    #Serchalble Fields..
    search_fields = ['name']


 
class DomainTable(viewsets.ModelViewSet):
    """
    You can performe filter based on 'name' field.
    """
    queryset = DomainTable.objects.all()
    serializer_class = DomainTableSerializer 

    #Apply Filter..
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    
    filterset_fields = ['name']
    #Apply Sorting..
    ordering_fields = ['name']
    #Serchalble Fields..
    search_fields = ['name']

class TagTable(viewsets.ModelViewSet):
    """
    Given a view instance, return a tag id and name to represent the view.
    name field you can use for filter.
    """
    queryset = TagTable.objects.all()
    serializer_class = TagTableSerializer 

    #Apply Filter..
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    
    filterset_fields = ['name']
    #Apply Sorting..
    ordering_fields = ['name']
    #Serchalble Fields..
    search_fields = ['name']

class CurrencyTable(viewsets.ModelViewSet):
    """
    You can performe filter based on name and iso field.
    """
    queryset = CurrencyTable.objects.all()
    serializer_class = CurrencyTableSerializer
    
    #Apply Filter..
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    
    filterset_fields = ['name','iso']
    #Apply Sorting..
    ordering_fields = ['name','iso']
    #Serchalble Fields..
    search_fields = ['name','iso']
 
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

#[END] 