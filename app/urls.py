from django.urls import path
from .views import *
app_name='app'
urlpatterns = [
    path('upload_files/',upload_files,name='upload_files'),
    # path('response/',llm_response,name='response'),
    path('',show_details,name='show_details'),
    path('push_json/',push_json,name='push_json'),
    path('show_csv/',show_csv,name='show_csv'),
]
