from django.forms import ModelForm, TextInput, Textarea, URLInput
from main.models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # Hanya gunakan field yang ada di Project model
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
                "class": "form-control"
            }),
            "description": Textarea(attrs={
                "placeholder": "Ceritakan tentang proyek ini...",
                "rows": 4,
                "class": "form-control"
            }),
            "tech_stack": TextInput(attrs={
                "placeholder": "Contoh: Django, Python, HTML, CSS",
                "class": "form-control"
            }),
            "project_url": URLInput(attrs={
                "placeholder": "https://github.com/username/project",
                "class": "form-control"
            }),
        }