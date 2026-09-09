from django.shortcuts import render
from main.models import Experience

def show_main(request):
    context = {
        "name": "Michelle Yuyun Margarethy Aritonang",
        "npm": "2506656961",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswi Sistem Informasi Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak, organisasi, dan desain."
        ),
    }
    return render(request, "index.html", context)

def show_experience(request):
    context = {
        "name": "Michelle Yuyun Margarethy Aritonang",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)