from django.urls import path
from main.views import (
    show_main, 
    show_experience, 
    show_projects, 
    create_project, 
    get_projects_json, 
    get_projects_xml,
    get_project_json_by_id,
    get_project_xml_by_id
)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('experience/', show_experience, name='show_experience'),
    path('projects/', show_projects, name='show_projects'),
    path('projects/add/', create_project, name='create_project'),
    
    # Rute Data Delivery (Semua & by ID)
    path('json/', get_projects_json, name='get_projects_json'),
    path('xml/', get_projects_xml, name='get_projects_xml'),
    path('json/<str:id>/', get_project_json_by_id, name='get_project_json_by_id'),
    path('xml/<str:id>/', get_project_xml_by_id, name='get_project_xml_by_id'),
]