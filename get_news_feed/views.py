import datetime
import json
import logging
import threading
import time

import requests
import schedule
from django.http import HttpResponse
from django.shortcuts import render

from rest_api.models import *
from get_news_feed.bing_search import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) 

def index(requests): 
    """
    default method 
    """
    bing_bot_two(11)   
    return HttpResponse("data=")

def start_job():
    """
    Call all marketplace apis...
    """
    print("Job runing...")
    get_active_project()   


def background_process():
    """
    This method call the api in every 10 minute.. 
    """
    schedule.every(10).minutes.do(start_job)        
    while True:
        schedule.run_pending()
        time.sleep(1)

def job_threading():
    """
    runing thread for api call  
    """
    t = threading.Thread(target=background_process, args=(), kwargs={})
    t.setDaemon(True)
    t.start()
    
 
#Bing API Call
def get_active_project():
    pass