from django.db import migrations


def clean_titles(apps, schema_editor):
    Project = apps.get_model('portfolio', 'Project')
    for project in Project.objects.all():
        if '(Team Project)' in project.title:
            project.title = project.title.replace('(Team Project)', '').strip()
            project.save(update_fields=['title'])


def reverse_clean_titles(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_alter_profile_linkedin_url_alter_skill_category'),
    ]

    operations = [
        migrations.RunPython(clean_titles, reverse_clean_titles),
    ]
