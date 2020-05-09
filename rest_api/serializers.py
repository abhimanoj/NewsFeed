from django.contrib.auth.models import User
from rest_framework import serializers
import datetime
from rest_api.models import *
  
class PersonTableSerializer(serializers.ModelSerializer):

    domain  = serializers.PrimaryKeyRelatedField(write_only=True,queryset=DomainTable.objects.all())
    currency = serializers.PrimaryKeyRelatedField(write_only=True,queryset=CurrencyTable.objects.all())
   
    class Meta:
        model = PersonTable
        fields = ('id', 'name', 'country', 'time_zone','_raw','domain','currency')
    
class DomainTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainTable
        fields = ('id', 'name', 'offer_description_max_length')

      
class TagTableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TagTable
        fields = ('id', 'name')
    
class CurrencyTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyTable
        fields = ('id', 'iso', 'name', 'symbol', 'iso')
    
class UserSerializer(serializers.HyperlinkedModelSerializer):
    rest_api = serializers.HyperlinkedRelatedField(
        many=True, view_name='rest_api-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'rest_api')
 