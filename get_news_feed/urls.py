from django.urls import path
from get_news_feed import views   

  
urlpatterns = [

    path('', views.index, name='index'),
]
 


