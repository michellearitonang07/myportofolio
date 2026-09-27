import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import ExperienceForm, ProjectForm
from main.models import Experience, Project

# --- AUTHENTICATION VIEWS ---

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Michelle Yuyun Margarethy Aritonang",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)

        response = redirect("main:show_main")
        response.set_cookie(
            "last_login",
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        return response

    context = {
        "name": "Michelle Yuyun Margarethy Aritonang",
        "form": form,
    }

    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response


def show_main(request):
    last_login = request.COOKIES.get(
        "last_login",
        "Belum ada sesi login / Cookie tidak ditemukan"
    )

    context = {
        "name": "Michelle Yuyun Margarethy Aritonang",
        "npm": "2506656961",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems student at Universitas Indonesia with a passion "
            "for software development, people management, and digital design. "
            "Enthusiastic about organizing events, building tech solutions, and driving impact."
        ),
        "last_login": last_login,
    }

    return render(request, "index.html", context)


# --- EXPERIENCE VIEWS ---

def show_experience(request):
    # 1. Ambil data Experience dari database
    raw_data = Experience.objects.all()

    # 2. Serialize objek Django menjadi JSON
    data_json = serializers.serialize("json", raw_data)

    # 3. Deserialize JSON kembali menjadi objek Django
    experience_list = [
        item.object
        for item in serializers.deserialize("json", data_json)
    ]

    context = {
        "name": "Michelle Yuyun Margarethy Aritonang",
        "experience_list": experience_list,
    }

    return render(request, "experience.html", context)


def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "form": form,
        "title": "Tambah Pengalaman",
    }

    return render(request, "experience_form.html", context)


def edit_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "form": form,
        "title": "Edit Pengalaman",
    }

    return render(request, "experience_form.html", context)


def delete_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


def get_experiences_json(request):
    experiences = Experience.objects.all()
    experiences_json = serializers.serialize("json", experiences)

    return HttpResponse(
        experiences_json,
        content_type="application/json"
    )


def get_experience_json_by_id(request, id):
    experience = Experience.objects.filter(pk=id)
    experience_json = serializers.serialize("json", experience)

    return HttpResponse(
        experience_json,
        content_type="application/json"
    )


# --- PROJECT VIEWS ---

def show_projects(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    context = {
        "name": "Michelle Yuyun Margarethy Aritonang",
        "project_list": projects,
        "title_query": title_query,
    }

    return render(request, "projects.html", context)


@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "form": form,
    }

    return render(request, "projects_form.html", context)


@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")


@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize(
        "json",
        projects,
        use_natural_foreign_keys=True
    )

    return HttpResponse(
        projects_json,
        content_type="application/json"
    )


def get_projects_xml(request):
    projects = Project.objects.all()
    projects_xml = serializers.serialize("xml", projects)

    return HttpResponse(
        projects_xml,
        content_type="application/xml"
    )


def get_project_json_by_id(request, id):
    project = Project.objects.filter(pk=id)
    project_json = serializers.serialize("json", project)

    return HttpResponse(
        project_json,
        content_type="application/json"
    )


def get_project_xml_by_id(request, id):
    project = Project.objects.filter(pk=id)
    project_xml = serializers.serialize("xml", project)

    return HttpResponse(
        project_xml,
        content_type="application/xml"
    )