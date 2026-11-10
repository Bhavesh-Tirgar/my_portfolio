import os
from pathlib import Path

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.management import call_command
from django.http import FileResponse, Http404, HttpResponse
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
    """Ensure database has initial portfolio data and admin superuser, without overwriting admin updates."""
    # Ensure superuser exists and credentials are valid
    try:
        admin_username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'bhavesh')
        admin_email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'tirgarbhavesh2005@gmail.com')
        admin_password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')

        user, created = User.objects.get_or_create(
            username=admin_username,
            defaults={'email': admin_email, 'is_staff': True, 'is_superuser': True}
        )
        if created or not user.is_superuser or not user.is_staff:
            user.is_staff = True
            user.is_superuser = True
            user.set_password(admin_password)
            user.save()
    except Exception:
        pass

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
        'google_site_verification': getattr(settings, 'GOOGLE_SITE_VERIFICATION', ''),
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


def robots_txt(request):
    sitemap_url = request.build_absolute_uri('/sitemap.xml')
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    base_url = request.build_absolute_uri('/')[:-1]
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{base_url}/</loc>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>{base_url}/about/</loc>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>{base_url}/projects/</loc>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>{base_url}/skills/</loc>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
    <url>
        <loc>{base_url}/education/</loc>
        <changefreq>monthly</changefreq>
        <priority>0.7</priority>
    </url>
    <url>
        <loc>{base_url}/contact/</loc>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
</urlset>"""
    return HttpResponse(xml.strip(), content_type="application/xml")


def google_verify_file(request, filename):
    full_name = filename if filename.startswith('google') else f"google{filename}"
    if full_name.endswith('.html'):
        return HttpResponse(f"google-site-verification: {full_name}", content_type="text/html")
    raise Http404()
