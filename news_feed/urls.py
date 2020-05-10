"""news_feed URL Configuration"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.schemas import get_schema_view
from get_news_feed.views import job_threading  


from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
schema_view = get_schema_view(title='news_feed backend', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    path('', include('rest_api.urls')),
    path('news_feed/', include('get_news_feed.urls')),


    path('admin/', admin.site.urls),

    path('v3/doc/', schema_view, name= 'v3.doc'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('news_feed', include('get_news_feed.urls')),
]

#Run for first time once server is start..for runing thread call api in every 10 minute..
job_threading()

