from pathlib import Path

from django import forms
from django.conf import settings
from django.contrib import messages
from django.core.management import call_command
from django.http import FileResponse, Http404
from django.shortcuts import render

from .models import ContactMessage, Education, Experience, Profile, Project, Skill


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your email'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Project inquiry'}),
            'message': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tell me about your project or opportunity'}),
        }


def seed_portfolio_data():
    """Ensure database has initial portfolio data if empty, without overwriting admin updates."""
    if not Profile.objects.exists() or not Project.objects.exists():
        try:
            call_command('seed_portfolio')
        except Exception:
            pass


def get_portfolio_context():
    seed_portfolio_data()
    profile = Profile.objects.first()
    return {
        'profile': profile,
        'skills': Skill.objects.all(),
        'education': Education.objects.all(),
        'projects': Project.objects.all(),
        'experiences': Experience.objects.all(),
    }


def render_page(request, template_name, extra_context=None):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message. I will get back to you soon.')
            form = ContactForm()

    context = get_portfolio_context()
    context['form'] = form
    if extra_context:
        context.update(extra_context)
    return render(request, template_name, context)


def home(request):
    return render_page(request, 'portfolio/home.html')


def about(request):
    return render_page(request, 'portfolio/about.html')


def projects(request):
    return render_page(request, 'portfolio/projects.html')


def skills(request):
    return render_page(request, 'portfolio/skills.html')


def education(request):
    return render_page(request, 'portfolio/education.html')


def contact(request):
    return render_page(request, 'portfolio/contact.html')


def resume_download(request):
    profile = Profile.objects.first()
    if profile and profile.resume_file:
        file = profile.resume_file
        return FileResponse(file.open('rb'), as_attachment=True, filename=Path(file.name).name)

    resume_path = Path(settings.BASE_DIR) / 'portfolio' / 'static' / 'portfolio' / 'files' / 'Bhavesh_Tirgar_Resume.pdf'
    if not resume_path.exists():
        raise Http404('Resume file not found.')

    return FileResponse(open(resume_path, 'rb'), as_attachment=True, filename='Bhavesh_Tirgar_Resume.pdf')
