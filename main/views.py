from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Exists, OuterRef, Value, BooleanField
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache

from main.forms import ExperienceForm, ProjectForm, EXPERIENCE_CATEGORY_LABELS
from main.models import Experience, Project
from main.life_snapshots import LIFE_SNAPSHOTS


# --- HELPER ROLE ---

def is_editor(user):
    return (
        user.is_authenticated
        and user.groups.filter(name="Editor").exists()
    )


# --- AUTHENTICATION VIEWS ---

def register(request):
    form = UserCreationForm(request.POST if request.method == "POST" else None)

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
    form = AuthenticationForm(request, data=request.POST if request.method == "POST" else None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)

        response = redirect("main:show_main")
        response.set_cookie(
            "last_login",
            timezone.localtime().strftime("%Y-%m-%d %H:%M:%S"),
            httponly=True,
            samesite="Lax",
            secure=settings.SESSION_COOKIE_SECURE,
        )
        return response

    context = {
        "name": "Michelle Yuyun Margarethy Aritonang",
        "form": form,
    }

    return render(request, "login.html", context)


@require_POST
def logout_user(request):
    logout(request)

    response = redirect("main:show_main")
    response.delete_cookie("last_login", samesite="Lax")

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
        "life_snapshots": LIFE_SNAPSHOTS,
    }

    return render(request, "index.html", context)


# --- EXPERIENCE VIEWS ---

def show_experience(request):
    raw_data = Experience.objects.all()

    data_json = serializers.serialize("json", raw_data)

    experience_list = [
        item.object
        for item in serializers.deserialize("json", data_json)
    ]

    context = {
        "name": "Michelle Yuyun Margarethy Aritonang",
        "experience_list": experience_list,
        "is_editor": is_editor(request.user),
    }

    return render(request, "experience.html", context)


@login_required(login_url="/login/")
def create_experience(request):
    # Hanya pemilik / superuser yang boleh membuat Experience
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ExperienceForm(request.POST if request.method == "POST" else None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "form": form,
        "title": "Tambah Pengalaman",
    }

    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def edit_experience(request, id):
    # Editor dan superuser boleh mengubah Experience
    if not (request.user.is_superuser or is_editor(request.user)):
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=id)
    form = ExperienceForm(request.POST if request.method == "POST" else None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "form": form,
        "title": "Edit Pengalaman",
    }

    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def delete_experience(request, id):
    # Hanya pemilik / superuser yang boleh menghapus Experience
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


@login_required(login_url="/login/")
@require_POST
def toggle_experience_star(request, id):
    experience = get_object_or_404(Experience, pk=id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")


@never_cache
def get_experiences_ajax(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.annotate(star_count=Count("starred_by")).order_by("-started_at", "id")
    if title_query:
        experiences = experiences.filter(title__icontains=title_query)
    if request.user.is_authenticated:
        starred = Experience.starred_by.through.objects.filter(
            experience_id=OuterRef("pk"), user_id=request.user.pk,
        )
        experiences = experiences.annotate(user_starred=Exists(starred))
    else:
        experiences = experiences.annotate(user_starred=Value(False, output_field=BooleanField()))

    # Kontrak baru tidak menyertakan identitas pemberi star atau data internal akun.
    data = [{
        "pk": str(experience.pk),
        "fields": {
            "title": experience.title,
            "description": experience.description,
            "category": experience.category,
            "category_label": EXPERIENCE_CATEGORY_LABELS.get(experience.category, experience.get_category_display()),
            "thumbnail": experience.thumbnail,
            "started_at": experience.started_at.isoformat(),
            "ended_at": experience.ended_at.isoformat() if experience.ended_at else None,
            "is_ongoing": experience.is_ongoing,
            "star_count": experience.star_count,
            "is_starred": experience.user_starred,
        },
    } for experience in experiences]
    return JsonResponse(data, safe=False)


@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan pengalaman. Silakan masuk dengan akun yang berhak."},
            status=403,
        )
    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse({"message": "Pengalaman berhasil ditambahkan.", "pk": str(experience.pk)}, status=201)
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


def get_experiences_json(request):
    experiences = Experience.objects.all()

    experiences_json = serializers.serialize(
        "json",
        experiences,
        use_natural_foreign_keys=True
    )

    return HttpResponse(
        experiences_json,
        content_type="application/json"
    )


def get_experience_json_by_id(request, id):
    experience = Experience.objects.filter(pk=id)

    experience_json = serializers.serialize(
        "json",
        experience,
        use_natural_foreign_keys=True
    )

    return HttpResponse(
        experience_json,
        content_type="application/json"
    )


# --- PROJECT VIEWS ---

def show_projects(request):
    context = {
        "name": "Michelle Yuyun Margarethy Aritonang",
        "title_query": request.GET.get("title", "").strip(),
        "form": ProjectForm(),
    }
    return render(request, "projects.html", context)


@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST if request.method == "POST" else None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "form": form,
    }

    return render(request, "projects_form.html", context)


@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.pk)},
            status=201,
        )
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


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
@require_POST
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")


@never_cache
def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related("starred_by").all()
    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []
    for project in projects:
        starred_users = list(project.starred_by.all())
        data.append({
            "pk": str(project.pk),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_url": project.project_url,
                "star_count": len(starred_users),
                "is_starred": request.user.is_authenticated and request.user in starred_users,
                "starred_by_names": ", ".join(user.username for user in starred_users),
            },
        })
    return JsonResponse(data, safe=False)


def get_projects_json_legacy(request):
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
    projects_xml = serializers.serialize("xml", projects, use_natural_foreign_keys=True)

    return HttpResponse(
        projects_xml,
        content_type="application/xml"
    )


def get_project_json_by_id(request, id):
    project = Project.objects.filter(pk=id)
    project_json = serializers.serialize("json", project, use_natural_foreign_keys=True)

    return HttpResponse(
        project_json,
        content_type="application/json"
    )


def get_project_xml_by_id(request, id):
    project = Project.objects.filter(pk=id)
    project_xml = serializers.serialize("xml", project, use_natural_foreign_keys=True)

    return HttpResponse(
        project_xml,
        content_type="application/xml"
    )