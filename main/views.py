from django.shortcuts import render
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