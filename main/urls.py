from django.urls import path
from main.views import (
    create_experience,
    create_project,
    delete_experience,
    delete_project,
    edit_experience,
    get_experience_json_by_id,
    get_experiences_json,
    get_project_json_by_id,
    get_project_xml_by_id,
    get_projects_json,
    get_projects_xml,
    show_experience,
    show_main,
    show_projects,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    
    # Experience
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:id>/edit/", edit_experience, name="edit_experience"),
    path("experience/<uuid:id>/delete/", delete_experience, name="delete_experience"),
    path("api/experience/", get_experiences_json, name="get_experiences_json"),
    path("api/experience/<uuid:id>/", get_experience_json_by_id, name="get_experience_json_by_id"),

    # Projects
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("json/", get_projects_json, name="get_projects_json_legacy"),
    path("xml/", get_projects_xml, name="get_projects_xml"),
    path("json/<uuid:id>/", get_project_json_by_id, name="get_project_json_by_id"),
    path("xml/<uuid:id>/", get_project_xml_by_id, name="get_project_xml_by_id"),
]