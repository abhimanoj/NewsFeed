import json

from django.db import models
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from django.utils import timezone
 
class DomainTable(models.Model): 
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=1000)
    offer_description_max_length =  models.IntegerField(db_column='offer_description_max_length', help_text="Define the max length of offer’s description allowed by the marketplace.")
    date_create = models.DateTimeField(db_column='date_create', default=timezone.now)
    date_update = models.DateTimeField(db_column='date_update', default=timezone.now)
   
    def __str__(self):
        domain_data = {}
        domain_data['id'] = self.id 
        domain_data['name'] = self.name
        domain_data['offer_description_max_length'] = self.offer_description_max_length 
        domain_data['date_create'] = str(self.date_create)
        domain_data['date_update'] = str(self.date_update)
        return json.dumps(domain_data)

    class Meta:
        ordering = ('date_create',)
        db_table = "domain"


class TagTable(models.Model): 
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=500)
    date_create = models.DateTimeField(db_column='date_create', default=timezone.now)
    date_update = models.DateTimeField(db_column='date_update', default=timezone.now)
    date_delete = models.DateTimeField(db_column='date_delete',  null=True, default=None)
       
    def __str__(self):
        tag_data = {}
        tag_data['id'] = self.id 
        tag_data['name'] = self.name 
         
        return json.dumps(tag_data)

    class Meta: 
        ordering = ('date_create',)
        db_table = "tag"

class CurrencyTable(models.Model): 
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=500)
    symbol = models.CharField(db_column='symbol', max_length=20)
    iso = models.CharField(db_column='iso', max_length=100)
    date_create = models.DateTimeField(db_column='date_create', default=timezone.now)
    date_update = models.DateTimeField(db_column='date_update', default=timezone.now)
    date_delete = models.DateTimeField(db_column='date_delete',  null=True, default=None)
       
    def __str__(self):
        currency_data = {}
        currency_data['id'] = self.id 
        currency_data['name'] = self.name
        currency_data['symbol'] = self.symbol
        currency_data['iso'] = self.iso 
         
        return json.dumps(currency_data)

    class Meta:
        ordering = ('date_create',)
        db_table = "currency"
 
class PersonTable(models.Model): 
    id = models.AutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=500)
    country =  models.CharField(db_column='country', max_length=200)
    time_zone = models.CharField(db_column='time_zone', max_length=100)
    date_create = models.DateTimeField(db_column='date_create', default=timezone.now)
    date_update = models.DateTimeField(db_column='date_update', default=timezone.now)
    date_delete = models.DateTimeField(db_column='date_delete',  null=True, default=None)
    _raw =  models.TextField(db_column="_raw", null=True, blank=True)
    domain = models.ForeignKey(DomainTable, related_name='dom_domain',  on_delete=models.CASCADE, help_text="FK on Domain")
    currency = models.ForeignKey(CurrencyTable, related_name='cur_currency', on_delete=models.CASCADE, help_text="FK on Currency (if the Person default Currency is specified)")
   
    def __str__(self):
        person_data = {}
        person_data['id'] = self.id 
        person_data['name'] = self.name
        person_data['country'] = self.country
        person_data['time_zone'] = self.time_zone  
        person_data['_raw'] = self._raw

        return json.dumps(person_data)

    class Meta:
        ordering = ('date_create',)
        db_table = "person"
 