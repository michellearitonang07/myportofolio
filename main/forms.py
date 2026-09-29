from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django.forms import ModelForm, TextInput, Textarea, Select, URLInput
from main.models import Project, Experience


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "tech_stack", "project_url"]
        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
        }
        widgets = {
            "title": TextInput(attrs={
                "placeholder": "Contoh: Portfolio Website",
                "class": "form-control",
            }),
            "description": Textarea(attrs={
                "placeholder": "Ceritakan tentang proyek ini...",
                "rows": 4,
                "class": "form-control",
            }),
            "tech_stack": TextInput(attrs={
                "placeholder": "Contoh: Django, Python, HTML, CSS",
                "class": "form-control",
            }),
            "project_url": URLInput(attrs={
                "placeholder": "https://github.com/username/project",
                "class": "form-control",
            }),
        }


    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_tech_stack(self):
        tech_stack = strip_tags(self.cleaned_data["tech_stack"]).strip()
        if not tech_stack:
            raise ValidationError("Teknologi tidak boleh hanya berisi tag HTML.")
        return tech_stack

    def clean_description(self):
        description = strip_tags(self.cleaned_data["description"]).strip()
        if not description:
            raise ValidationError("Deskripsi tidak boleh hanya berisi tag HTML.")
        return description


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ["title", "description", "category", "thumbnail", "ended_at"]
        labels = {
            "title": "Judul Pengalaman",
            "description": "Deskripsi",
            "category": "Kategori",
            "thumbnail": "URL Gambar/Thumbnail",
            "ended_at": "Tanggal Selesai",
        }
        widgets = {
            "title": TextInput(attrs={
                "placeholder": "Contoh: Staff Human Resources",
                "class": "form-control",
            }),
            "description": Textarea(attrs={
                "placeholder": "Jelaskan peran dan kontribusimu...",
                "rows": 4,
                "class": "form-control",
            }),
            "category": Select(attrs={
                "class": "form-control",
            }),
            "thumbnail": URLInput(attrs={
                "placeholder": "https://example.com/image.png",
                "class": "form-control",
            }),
            "ended_at": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                },
                format="%Y-%m-%dT%H:%M",
            ),
        }