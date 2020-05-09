import datetime
import json

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from news_feed.views import *
from rest_api.models import *

baseurl = "https://www.bing.com" 

#
#   [BEGIN] Exemple of standard unit tests
#   Note : build test from specifications requirements, not from the current result
#
class TestInitiator(TestCase):
    """
    TestCase middleware : allow to initialize globalily setUp()
    """
    def setUp(self):
        
        temp_date = datetime.datetime.now().isoformat()

        # Domain
        DomainTable.objects.create(id =1, name='BING_1', offer_description_max_length=101, date_create=temp_date, date_update=temp_date)
        DomainTable.objects.create(id =2, name='BING_2', offer_description_max_length=102, date_create=temp_date, date_update=temp_date)
        DomainTable.objects.create(id =3, name='BING_3', offer_description_max_length=103, date_create=temp_date, date_update=temp_date)
        
        # Currency
        CurrencyTable.objects.create(id=1, name='Euro', symbol='1', iso='EUR', date_create=temp_date, date_update=temp_date, date_delete=temp_date)
        CurrencyTable.objects.create(id=2, name='US Dollar', symbol='2', iso='USD', date_create=temp_date, date_update=temp_date, date_delete=temp_date)
        CurrencyTable.objects.create(id=3, name='Ruppee', symbol='3', iso='INR', date_create=temp_date, date_update=temp_date, date_delete=temp_date)

        # Tag
        TagTable.objects.create(id =1, name='tag#1', date_create=temp_date, date_update=temp_date, date_delete=temp_date)
        TagTable.objects.create(id =2, name='tag#2', date_create=temp_date, date_update=temp_date, date_delete=temp_date)
        TagTable.objects.create(id =3, name='tag_is', date_create=temp_date, date_update=temp_date, date_delete=temp_date)

        # Get [domain_id] 
        domain_id_1 = DomainTable.objects.get(name='BING_1').id      
        domain_id_2 = DomainTable.objects.get(name='BING_2').id     
        domain_id_3 = DomainTable.objects.get(name='BING_3').id      
        
        # Get [currency_id]
        currency_id_1 = CurrencyTable.objects.get(symbol=1).id
        currency_id_2 = CurrencyTable.objects.get(symbol=2).id
        currency_id_3 = CurrencyTable.objects.get(symbol=3).id
        
        # Person
        PersonTable.objects.create(id =1, name='user_1', country='test', time_zone='24' , date_create=temp_date, date_update=temp_date, date_delete=temp_date, _raw='raw data', domain_id=domain_id_1, currency_id = currency_id_1)
        PersonTable.objects.create(id =2, name='user_2', country='test', time_zone='24' , date_create=temp_date, date_update=temp_date, date_delete=temp_date, _raw='raw data', domain_id=domain_id_2, currency_id = currency_id_2)
        PersonTable.objects.create(id =3, name='user_3', country='test', time_zone='24' , date_create=temp_date, date_update=temp_date, date_delete=temp_date, _raw='raw data', domain_id=domain_id_3, currency_id = currency_id_3)
 

class TestRestApiDomain(TestInitiator):
    """
    For test all features of Domain REST API
    """

    #
    #   REST
    #
    def test_get(self):
        """ Test GET API """

        # Create an instance of a GET request.
        result_1 = Client().get('/Domain/1/', content_type= 'application/json')
        result_2 = Client().get('/Domain/2/', content_type= 'application/json')
        result_3 = Client().get('/Domain/3/', content_type= 'application/json')
       
        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual(result_2.status_code, status.HTTP_200_OK)
        self.assertEqual(result_3.status_code, status.HTTP_200_OK)

        self.assertEqual(result_1.json()['offer_description_max_length'], 101) # will raise an exception if "Content-Type" header is not "application/json"
        self.assertEqual(result_2.json()['offer_description_max_length'], 102) # will raise an exception if "Content-Type" header is not "application/json"
        self.assertEqual(result_3.json()['offer_description_max_length'], 103) # will raise an exception if "Content-Type" header is not "application/json"

    def test_list(self):
        """ Test list API """
     
        # Create an instance of a GET request.
        list_data = Client().get('/Domain/', content_type= 'application/json')
      
        self.assertEqual(list_data.status_code, status.HTTP_200_OK)
        self.assertEqual(list_data.json()['count'], 3) 

    def test_put(self):
        """ Test PUT API """

        payload = {"name": "BING_4","offer_description_max_length":200}
        Client().put(path='/Domain/2/', data=payload, content_type= 'application/json')

        #Get the updated result and verify..
        result_1 = Client().get('/Domain/2/', content_type= 'application/json')

        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual(result_1.json()['name'], 'BING_4') 
      
    def test_patch(self):
        """ Test PATCH API """  
        payload = {"name": "BING_4"}
        Client().patch(path='/Domain/1/', data=payload, content_type= 'application/json')
        
        #Get the updated result and verify..
        result_1 = Client().get('/Domain/1/', content_type= 'application/json')

        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual(result_1.json()['name'], 'BING_4') 


    #
    #   Features
    #
    def test_sort(self):
        """ Test sorting feature """

        #Sort data by date_create
        result = Client().get('/Domain/?ordering=-name', content_type= 'application/json')
   
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        
        index = 3
        for result_data in result.json()['results']:
            #test in accending order..
            self.assertEqual(result_data['id'], index)
            index -= 1
        
    def test_pagination(self):
        """ Test pagination feature """
        result_1 = Client().get('/Domain/?limit=1', content_type= 'application/json')
       
        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual(result_1.json()['next'], 'http://testserver/Domain/?limit=1&offset=1')
    

    def test_filter(self):
        """ Test filtering API """
        result_1 = Client().get('/Domain/?search=BING_1', content_type= 'application/json')
        
        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual((result_1.json()['results'])[0]['name'], 'BING_1')
    

class TestRestApiCurrency(TestInitiator):
    """
    For test all features of Currency REST API
    """

    #
    #   REST
    #

    def test_get(self):
        """ Test GET API """
        result_1 = Client().get('/Currency/1/', content_type= 'application/json')
        result_2 = Client().get('/Currency/2/', content_type= 'application/json')
        result_3 = Client().get('/Currency/3/', content_type= 'application/json')

        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual(result_2.status_code, status.HTTP_200_OK)
        self.assertEqual(result_3.status_code, status.HTTP_200_OK)
       
        self.assertEqual(result_1.json()['name'], 'Euro') # will raise an exception if "Content-Type" header is not "application/json"
        self.assertEqual(result_2.json()['name'], 'US Dollar') # will raise an exception if "Content-Type" header is not "application/json"
        self.assertEqual(result_3.json()['name'], 'Ruppee') # will raise an exception if "Content-Type" header is not "application/json"

    def test_list(self):
        """ Test list API """
     
        # Create an instance of a GET request.
        list_data = Client().get('/Currency/', content_type= 'application/json')
      
        self.assertEqual(list_data.status_code, status.HTTP_200_OK)
        self.assertEqual(list_data.json()['count'], 3) 

    def test_put(self):
        """ Test PUT API """

        payload = {"name": "Pound","symbol":"3", "iso":"USD" }
        Client().put(path='/Currency/1/', data=payload, content_type= 'application/json')
        
        #Get the updated result and verify..
        result_1 = Client().get('/Currency/1/', content_type= 'application/json')

        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual(result_1.json()['name'], 'Pound') 

    def test_patch(self):
        """ Test PATCH API """
    
        payload = {"name": "Pound"}
        Client().patch(path='/Currency/1/', data=payload, content_type= 'application/json')

        #Get the updated result and verify..
        result_1 = Client().get('/Currency/1/', content_type= 'application/json')
        
        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual(result_1.json()['name'], 'Pound') 

    #
    #   Features
    #
    def test_sort(self):
        """ Test sorting feature """
        
        #Sort data by date_create
        result = Client().get('/Currency/?ordering=-name', content_type= 'application/json')
   
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        
        index = 3
        for result_data in result.json()['results']:
            #test in accending order..
            if index == 3:
                self.assertEqual(result_data['name'], 'US Dollar')

            if index == 2:
                self.assertEqual(result_data['name'], 'Ruppee')
    
            if index == 1:
                self.assertEqual(result_data['name'], 'Euro')

            index -= 1

    def test_pagination(self):
        """ Test pagination feature """
        result_1 = Client().get('/Currency/?limit=1', content_type= 'application/json')

        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual(result_1.json()['next'], 'http://testserver/Currency/?limit=1&offset=1')
        

    def test_filter(self):
        """ Test filtering API """
        result_1 = Client().get('/Currency/?iso=INR', content_type= 'application/json')
        
        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual((result_1.json()['results'])[0]['iso'], 'INR')
    

class TestRestApiTag(TestInitiator):
    """
    For test all features of Tag REST API
    """

    #
    #   REST
    #

    def test_get(self):
        """ Test GET API """
        result_1 = Client().get('/Tag/1/', content_type= 'application/json')
        result_2 = Client().get('/Tag/2/', content_type= 'application/json')
        result_3 = Client().get('/Tag/3/', content_type= 'application/json')

        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual(result_2.status_code, status.HTTP_200_OK)
        self.assertEqual(result_3.status_code, status.HTTP_200_OK)
        
        self.assertEqual(result_1.json()['name'], 'tag#1') # will raise an exception if "Content-Type" header is not "application/json"
        self.assertEqual(result_2.json()['name'], 'tag#2') # will raise an exception if "Content-Type" header is not "application/json"
        self.assertEqual(result_3.json()['name'], 'tag_is') # will raise an exception if "Content-Type" header is not "application/json"

    def test_list(self):
        """ Test list API """
     
        # Create an instance of a GET request.
        list_data = Client().get('/Tag/', content_type= 'application/json')
      
        self.assertEqual(list_data.status_code, status.HTTP_200_OK)
        self.assertEqual(list_data.json()['count'], 3) 


    def test_put(self):
        """ Test PUT API """ 

        payload = {"name": "tag#11"}
        Client().put(path='/Tag/1/', data=payload, content_type= 'application/json')
        
        #Get the updated result and verify..
        result_1 = Client().get('/Tag/1/', content_type= 'application/json')

        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual(result_1.json()['name'], 'tag#11') 

    def test_patch(self):
        """ Test PATCH API """
    
        payload = {"name": "tag#11"}
        Client().patch(path='/Tag/1/', data=payload, content_type= 'application/json')

        #Get the updated result and verify..
        result_1 = Client().get('/Tag/1/', content_type= 'application/json')
 
        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual(result_1.json()['name'], 'tag#11') 


    #
    #   Features
    #
    def test_sort(self):
        """ Test sorting feature """
        
        #Sort data by date_create
        result = Client().get('/Tag/?ordering=-name', content_type= 'application/json')
   
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        
        index = 3
        for result_data in result.json()['results']:
            #test in accending order..
            self.assertEqual(result_data['id'], index)
            index -= 1

    def test_pagination(self):
        """ Test pagination feature """
        result_1 = Client().get('/Tag/?limit=1', content_type= 'application/json')

        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual(result_1.json()['next'], 'http://testserver/Tag/?limit=1&offset=1')

    def test_filter(self):
        """ Test filtering API """
        result_1 = Client().get('/Tag/?search=tag_is', content_type= 'application/json')

        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual((result_1.json()['results'])[0]['name'], 'tag_is')

class TestRestApiPerson(TestInitiator):
    """
    For test all features of Person REST API
    """

    #
    #   REST
    #

    def test_get(self):
        """ Test GET API """
        result_1 = Client().get('/Person/1/', content_type= 'application/json')
        result_2 = Client().get('/Person/2/', content_type= 'application/json')
        result_3 = Client().get('/Person/3/', content_type= 'application/json')
       
        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual(result_2.status_code, status.HTTP_200_OK)
        self.assertEqual(result_3.status_code, status.HTTP_200_OK)
        self.assertEqual(result_1.json()['name'], 'user_1') # will raise an exception if "Content-Type" header is not "application/json"
        self.assertEqual(result_2.json()['name'], 'user_2') # will raise an exception if "Content-Type" header is not "application/json"
        self.assertEqual(result_3.json()['name'], 'user_3') # will raise an exception if "Content-Type" header is not "application/json"


    def test_list(self):
        """ Test list API """
     
        # Create an instance of a GET request.
        list_data = Client().get('/Person/', content_type='application/json')
      
        self.assertEqual(list_data.status_code, status.HTTP_200_OK)
        self.assertEqual(list_data.json()['count'], 3) 

    def test_put(self):
        """ Test PUT API """
      
        payload = {"name": "update_user_1", "country":"test", "time_zone":"24"}
        Client().patch(path='/Person/1/', data=payload, content_type= 'application/json')
        
        #Get the updated result and verify..
        result_1 = Client().get('/Person/1/', content_type= 'application/json')

        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual(result_1.json()['name'], 'update_user_1') 


    def test_patch(self):
        """ Test PATCH API """
     
        payload = {"name": "update_user_1"}
        Client().patch(path='/Person/1/', data=payload, content_type= 'application/json')
        
        #Get the updated result and verify..
        result_1 = Client().get('/Person/1/', content_type= 'application/json')

        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual(result_1.json()['name'], 'update_user_1') 


    #
    #   Features
    #
    def test_sort(self):
        """ Test sorting feature """
        
        #Get Sorted data by name
        result = Client().get('/Person/?ordering=-name', content_type= 'application/json')
   
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        
        index = 3
        for result_data in result.json()['results']:
            #test in accending order..
            self.assertEqual(result_data['id'], index)
            index -= 1

    def test_pagination(self):
        """ Test pagination feature """
        result_1 = Client().get('/Person/?limit=1', content_type= 'application/json')
       
        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual(result_1.json()['next'], 'http://testserver/Person/?limit=1&offset=1')

    def test_filter(self):
        """ Test filtering API """
        result_1 = Client().get('/Person/?name=user_1', content_type= 'application/json')

        self.assertEqual(result_1.status_code, status.HTTP_200_OK)
        self.assertEqual((result_1.json()['results'])[0]['name'], 'user_1')

 
#Test Post Method..
class TestModelDomainPost(TestCase):   
    
    def test_post(self):
        """ Test POST API """  

        temp_date = datetime.datetime.now().isoformat()

        payload = {'name': 'FREELANCER_4', 'offer_description_max_length':102,'date_create':temp_date, 'date_update':temp_date}
        result_1 = Client().post(path='/Domain/', data=json.dumps(payload), content_type= 'application/json')
         
        self.assertEqual(result_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result_1.json()['name'], 'FREELANCER_4')

class TestModelCurrencyPost(TestCase):   
 
    def test_post(self):
        """ Test POST API """  

        temp_date = datetime.datetime.now().isoformat()
        payload = {'name': 'Pound','symbol':'3', 'iso':'USD','date_create':temp_date, 'date_update':temp_date}
        result_1 = Client().post(path='/Currency/', data=json.dumps(payload), content_type= 'application/json')
   
        self.assertEqual(result_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result_1.json()['name'], 'Pound') 


class TestModelTagPost(TestCase):  
    
    def test_post(self):
        """ Test POST API """  

        temp_date = datetime.datetime.now().isoformat()
        payload = {'name': 'tag#11','date_create':temp_date, 'date_update':temp_date}
        result_1 = Client().post(path='/Tag/', data=json.dumps(payload), content_type= 'application/json')
 
        self.assertEqual(result_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result_1.json()['name'], 'tag#11') 
 
class TestModelPersonPost(TestCase):   

    def test_post(self):
        """ Test POST API """  

        temp_date = datetime.datetime.now().isoformat()
        payload = {'name': 'Pound','symbol':'3', 'iso':'USD','date_create':temp_date, 'date_update':temp_date}
        result = Client().post(path='/Currency/', data=json.dumps(payload), content_type='application/json')
        
        #Get [currency_id]
        currency_id = result.json()['id']
        
        payload = {'name': 'FREELANCER_4', 'offer_description_max_length':102,'date_create':temp_date, 'date_update':temp_date}
        result_ = Client().post(path='/Domain/', data=json.dumps(payload), content_type='application/json')
         
        #Get [domain_id]
        domain_id = result_.json()['id']


        payload = {'name': 'new_user_1', 'country':'test', 'time_zone':'24', 'date_create':temp_date, 'date_update':temp_date, 'date_delete':temp_date , '_raw':'raw data', 'domain':domain_id, 'currency':currency_id}
        result_1 = Client().post(path='/Person/', data=json.dumps(payload), content_type='application/json')
         
        self.assertEqual(result_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result_1.json()['name'], 'new_user_1') 

#
#   [END] Exemple of standard unit tests
#


class TestModelDomain(TestCase):   
    """
    Test Domain table Insert and  Getting the row...
    """

    def setUp(self):
        temp_date = datetime.datetime.now().isoformat()
        DomainTable.objects.create(id =1, offer_description_max_length=100, date_create=temp_date, date_update=temp_date)
        DomainTable.objects.create(id =2, offer_description_max_length=100, date_create=temp_date, date_update=temp_date)
        DomainTable.objects.create(id =3, offer_description_max_length=100, date_create=temp_date, date_update=temp_date)
      
    def test_domain(self):
        domain_single = DomainTable.objects.get(id=1)
        domain_single2 = DomainTable.objects.get(id=2)
        domain_single3 = DomainTable.objects.get(id=3)
        

        self.assertEqual(domain_single  .id, 1) 
        self.assertEqual(domain_single2.id, 2)  
        self.assertEqual(domain_single3.id, 3)  
       

class TestModelCurrencyTable(TestCase):   
    """
    Test currency table Insert and  Getting the row...
    """

    def setUp(self):
        temp_date = datetime.datetime.now().isoformat()
        CurrencyTable.objects.create(id=1, name='Unit Test', symbol='', iso='', date_create=temp_date, date_update=temp_date, date_delete=temp_date)
        CurrencyTable.objects.create(id=2, name='Unit Test', symbol='', iso='', date_create=temp_date, date_update=temp_date, date_delete=temp_date)
        CurrencyTable.objects.create(id=3, name='Unit Test', symbol='', iso='', date_create=temp_date, date_update=temp_date, date_delete=temp_date)
       
    def test_currency(self):
        currency_single = CurrencyTable.objects.get(id=1)
        currency_single1 = CurrencyTable.objects.get(id=2)
        currency_single2 = CurrencyTable.objects.get(id=3)
      
        
        self.assertEqual(currency_single.id, 1)
        self.assertEqual(currency_single1.id, 2)
        self.assertEqual(currency_single2.id, 3)
       
class TestModelTagTable(TestCase):   
    """
    Test TagTable model with insert and get the single row..
    """

    def setUp(self):
        temp_date = datetime.datetime.now().isoformat()
        TagTable.objects.create(id =1, name='test name', date_create=temp_date, date_update=temp_date, date_delete=temp_date)
        TagTable.objects.create(id =2, name='test name', date_create=temp_date, date_update=temp_date, date_delete=temp_date)
        TagTable.objects.create(id =3, name='test name', date_create=temp_date, date_update=temp_date, date_delete=temp_date)
         
    def test_person(self):
        tag_row = TagTable.objects.get(id=1)
        tag_row1 = TagTable.objects.get(id=2)
        tag_row2 = TagTable.objects.get(id=3)
        
        
        self.assertEqual(tag_row.id, 1)
        self.assertEqual(tag_row1.id, 2)
        self.assertEqual(tag_row2.id, 3)
 
class TestModelPersonTable(TestCase):   
    """
    Test PersonTable model with insert and get the single row..
    """
   
    def setUp(self):
        temp_date = datetime.datetime.now().isoformat()
        CurrencyTable.objects.create(id=2, name='Unit Test', symbol='', iso='', date_create=temp_date, date_update=temp_date, date_delete=temp_date)
        DomainTable.objects.create(id =1, name='BING', offer_description_max_length=100, date_create=temp_date, date_update=temp_date)

        #get domain id
        domain_id = DomainTable.objects.latest('id').id

        #get currency id
        currency_id = CurrencyTable.objects.latest('id').id
        
        PersonTable.objects.create(id =1, name='test name', country='test', time_zone='24' , date_create=temp_date, date_update=temp_date, date_delete=temp_date, _raw='raw data', domain_id=domain_id, currency_id = currency_id)

    def test_person(self):
        person_single = PersonTable.objects.get(id=1)
        
        self.assertEqual(person_single.id, 1)
 
#Test Freelance api..
class TestBingApiGetProject(TestCase):   

    def test_get_project(self): 
 
        url = baseurl + "/news/search?q=technology"
    
        headers = get_auth_header(default_auth_token)  
         
        response = requests.request("GET", url, headers=headers)
    
        re_code = response.status_code
          
        self.assertEqual(re_code, status.HTTP_200_OK)
