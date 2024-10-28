from django.urls import path
from .views import *
app_name='app'
urlpatterns = [
    path('show_csv/',show_csv,name='show_csv'),
    path('download_csv/',download_csv,name='download_csv'),
    path('',formView,name='formview'),
    path('getFormData/',getFormData,name='getFormData'),
    path('push_webhook/',push_webhook,name='push_webhook'),
    path('db/',database,name='database'),
]
