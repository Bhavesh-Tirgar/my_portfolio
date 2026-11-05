import os
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from portfolio.models import Education, Experience, Profile, Project, Skill


class Command(BaseCommand):
    help = 'Populate the portfolio website with resume profile data and default admin user.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force re-seeding and overwrite existing portfolio records',
        )

    def handle(self, *args, **options):
        force = options.get('force', False)

        # 1. Admin Superuser
        admin_username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'bhavesh')
        admin_email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'tirgarbhavesh2005@gmail.com')
        admin_password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')

        user, created = User.objects.get_or_create(
            username=admin_username,
            defaults={'email': admin_email, 'is_staff': True, 'is_superuser': True}
        )
        user.is_staff = True
        user.is_superuser = True
        user.email = admin_email
        user.set_password(admin_password)
        user.save()
        if created:
            self.stdout.write(self.style.SUCCESS(f'Superuser "{admin_username}" created with password "{admin_password}".'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser "{admin_username}" password set to "{admin_password}".'))

        # 2. Profile
        if force or not Profile.objects.exists():
            Profile.objects.update_or_create(
                full_name='Bhavesh Tirgar',
                defaults={
                    'headline': 'MCA Student | Python & Backend Developer (Django, Laravel, SQL, MongoDB)',
                    'short_bio': 'MCA student (Semester 3) at Gujarat Vidyapith and Python developer experienced with Django, Laravel, SQL and MongoDB. Completed a CodeAlpha Python internship, built a full-stack plan-based education platform, and worked in teams on AI, agentic AI and Odoo-based projects through Git and GitHub. Seeking a Python developer or backend role.',
                    'email': 'tirgarbhavesh2005@gmail.com',
                    'phone': '9313865016',
                    'location': 'Gujarat, India',
                    'github_url': 'https://github.com/Bhavesh-Tirgar',
                    'linkedin_url': 'https://in.linkedin.com/in/bhavesh-tirgar-1734b4286',
                },
            )
            self.stdout.write(self.style.SUCCESS('Profile seeded.'))

        # 3. Skills
        if force or not Skill.objects.exists():
            if force:
                Skill.objects.all().delete()
            Skill.objects.bulk_create([
                Skill(name='Python', category='Language', proficiency=95, order=1),
                Skill(name='Django', category='Backend', proficiency=92, order=2),
                Skill(name='Laravel', category='Backend', proficiency=88, order=3),
                Skill(name='PHP', category='Backend', proficiency=86, order=4),
                Skill(name='SQL & MySQL', category='Database', proficiency=90, order=5),
                Skill(name='MongoDB', category='Database', proficiency=85, order=6),
                Skill(name='Oracle 11g', category='Database', proficiency=82, order=7),
                Skill(name='Agentic AI & AI', category='AI', proficiency=90, order=8),
                Skill(name='JavaScript', category='Frontend', proficiency=86, order=9),
                Skill(name='Tailwind CSS & Bootstrap', category='Frontend', proficiency=90, order=10),
                Skill(name='HTML & CSS / jQuery', category='Frontend', proficiency=92, order=11),
                Skill(name='Git & GitHub', category='Tools', proficiency=94, order=12),
                Skill(name='Odoo', category='Tools', proficiency=85, order=13),
                Skill(name='VS Code & Jupyter', category='Tools', proficiency=92, order=14),
                Skill(name='C', category='Language', proficiency=80, order=15),
            ])
            self.stdout.write(self.style.SUCCESS('Skills seeded.'))

        # 4. Education
        if force or not Education.objects.exists():
            if force:
                Education.objects.all().delete()
            Education.objects.bulk_create([
                Education(
                    institution='Gujarat Vidyapith',
                    degree='Master of Computer Applications (MCA)',
                    period='2025 - 2027 (Sem 3)',
                    description='Focused on advanced software engineering, backend architectures, AI systems, and database engineering.',
                    location='Gujarat, India',
                    is_current=True,
                    order=1,
                ),
                Education(
                    institution='Smt. C.S.S. BCA College, Deesa',
                    degree='Bachelor of Computer Application (BCA)',
                    period='2022 - 2025',
                    description='Graduated with CGPA 7.19/10. Comprehensive foundation in computer science, software logic, and web systems.',
                    location='Deesa, Gujarat',
                    is_current=False,
                    order=2,
                ),
                Education(
                    institution='Shree Maharshi Krnva, Abhinav Vidhyalay, Bapla',
                    degree='Higher Secondary (12th)',
                    period='2022',
                    description='Higher secondary schooling with 65.00% score.',
                    location='Bapla, Gujarat',
                    is_current=False,
                    order=3,
                ),
                Education(
                    institution='Shree Maharshi Krnva, Abhinav Vidhyalay, Bapla',
                    degree='Secondary (10th)',
                    period='2020',
                    description='Secondary schooling with 50.00% score.',
                    location='Bapla, Gujarat',
                    is_current=False,
                    order=4,
                ),
            ])
            self.stdout.write(self.style.SUCCESS('Education seeded.'))

        # 5. Projects (The 5 checked projects from GitHub screenshots & resume)
        if force or not Project.objects.exists():
            if force:
                Project.objects.all().delete()
            Project.objects.bulk_create([
                Project(
                    title='Digital Academy - Online Education Platform',
                    slug='digital-academy',
                    summary='Full-stack platform with plan-based access (Basic, Standard, Premium) to video lectures, PDFs, and handwritten notes.',
                    description='Built a full-stack platform with plan-based access (Basic, Standard, Premium) to videos, PDFs and handwritten notes. Created an admin panel and responsive dashboard to manage courses, subjects and study materials without changing existing database tables. Implemented role-based authentication, secure Blade templates, restricted file access and dynamic subject-wise and plan-wise filters.',
                    technologies='Laravel, PHP, MySQL, HTML, CSS, jQuery',
                    github_url='https://github.com/Bhavesh-Tirgar/digital_academy',
                    featured=True,
                    order=1,
                ),
                Project(
                    title='FleetFlow - Fleet Management (Team Project)',
                    slug='odoo-fleetflow',
                    summary='Modular fleet tracking and operations management module built on the Odoo enterprise platform.',
                    description='Collaborated with a development team to build a fleet management module on the Odoo platform, managing vehicle operations, maintenance schedules, and route coordination using Git and GitHub for team collaboration.',
                    technologies='Odoo, Python, XML, PostgreSQL',
                    github_url='https://github.com/Narendra-Purohit/odoo-fleetflow',
                    featured=True,
                    order=2,
                ),
                Project(
                    title='IntelliSchedule-AI (Team Project)',
                    slug='intellischedule-ai',
                    summary='Automated scheduling solution powered by AI algorithms for optimized timetable and task planning.',
                    description='Contributed to an AI-based scheduling project as part of a development team, developing logic in Python and utilizing a shared GitHub repository for collaborative sprint delivery.',
                    technologies='AI, Python, Git',
                    github_url='https://github.com/Narendra-Purohit/IntelliSchedule-AI',
                    featured=True,
                    order=3,
                ),
                Project(
                    title='Agentic AI Project (Team Project)',
                    slug='agentic-ai-project',
                    summary='Autonomous AI agent system designed for intelligent task orchestration and automated reasoning.',
                    description='Collaborated with a teammate on an agentic AI project, implementing autonomous agents, tool interaction loops, and structured LLM outputs through a shared GitHub repository.',
                    technologies='Agentic AI, Python, LLMs',
                    github_url='https://github.com/Hardik-RS/Agentic_AI_Project',
                    featured=True,
                    order=4,
                ),
                Project(
                    title='PLM Eco System (Team Project)',
                    slug='plm-eco-system',
                    summary='Product Lifecycle Management (PLM) and Engineering Change Order (ECO) system on Odoo.',
                    description='Collaborated with a team on a product lifecycle management (PLM) and engineering change order (ECO) system on Odoo, structuring workflows, version controls, and engineering status approvals.',
                    technologies='Odoo, PLM, Python, PostgreSQL',
                    github_url='https://github.com/Narendra-Purohit/plm-eco-system',
                    featured=True,
                    order=5,
                ),
            ])
            self.stdout.write(self.style.SUCCESS('Projects seeded.'))

        # 6. Experience
        if force or not Experience.objects.exists():
            if force:
                Experience.objects.all().delete()
            Experience.objects.bulk_create([
                Experience(
                    title='Python Programming Intern',
                    company='CodeAlpha (ID: CA/JU3/2817)',
                    period='2025',
                    description='Completed assigned Python projects, including a stock tracker application, and published them in a version-controlled GitHub repository.',
                    type='Internship',
                    order=1,
                ),
                Experience(
                    title='Technical Workshop Lead & Organizer',
                    company='Technical Workshops (100+ Students)',
                    period='2024 - 2025',
                    description='Organized and managed 4+ technical workshops for 100+ students on Web Development, Cyber Security & Ethical Hacking, Data Analytics, and Advanced Excel, handling everything from planning to execution.',
                    type='Academic',
                    order=2,
                ),
                Experience(
                    title='Google Student Certified Developer',
                    company='Google Certification & Academic Projects',
                    period='2024 - 2026',
                    description='Earned Google Student Certificate and developed modern software projects in Python, Django, Laravel, and Agentic AI systems.',
                    type='Academic',
                    order=3,
                ),
            ])
            self.stdout.write(self.style.SUCCESS('Experience seeded.'))

        self.stdout.write(self.style.SUCCESS('Portfolio data check complete.'))
