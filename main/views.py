from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import redirect, render

from main.forms import ProjectForm
from main.models import Experience, Project  


def show_main(request):
    context = {
        "name": "Michelle Yuyun Margarethy Aritonang",
        "npm": "2506656961",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems student at Universitas Indonesia with a passion "
            "for software development, people management, and digital design. "
            "Enthusiastic about organizing events, building tech solutions, and driving impact."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Michelle Yuyun Margarethy Aritonang",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_projects(request):
    context = {
        "name": "Michelle Yuyun Margarethy Aritonang",
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)


def create_project(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {"form": form}
    return render(request, "projects_form.html", context)


# =========================================================
# BAGIAN 3: DATA DELIVERY (JSON & XML API)
# =========================================================

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()
    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")


def get_projects_xml(request):
    projects = Project.objects.all()
    projects_xml = serializers.serialize("xml", projects)
    return HttpResponse(projects_xml, content_type="application/xml")

def get_project_json_by_id(request, id):
    project = Project.objects.filter(pk=id)
    project_json = serializers.serialize("json", project)
    return HttpResponse(project_json, content_type="application/json")

def get_project_xml_by_id(request, id):
    project = Project.objects.filter(pk=id)
    project_xml = serializers.serialize("xml", project)
    return HttpResponse(project_xml, content_type="application/xml")