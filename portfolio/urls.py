from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('skills/', views.skills, name='skills'),
    path('education/', views.education, name='education'),
    path('contact/', views.contact, name='contact'),
    path('resume/download/', views.resume_download, name='resume_download'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('google<str:filename>', views.google_verify_file, name='google_verify_file'),
]
