from django.contrib.auth.models import User
from django.core import mail
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse

from portfolio.models import ContactMessage, Education, Experience, Profile, Project, Skill


class PortfolioViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Seed initial data for testing
        call_command('seed_portfolio')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/home.html')
        self.assertIn('profile', response.context)
        self.assertIn('projects', response.context)
        self.assertIn('skills', response.context)
        self.assertContains(response, 'Bhavesh Tirgar')

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/about.html')
        self.assertContains(response, 'Gujarat Vidyapith')

    def test_projects_view(self):
        response = self.client.get(reverse('projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/projects.html')
        # Assert the 5 curated projects are present
        self.assertEqual(Project.objects.count(), 5)
        self.assertContains(response, 'Digital Academy')
        self.assertContains(response, 'FleetFlow')

    def test_skills_view(self):
        response = self.client.get(reverse('skills'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/skills.html')
        self.assertTrue(Skill.objects.filter(name='Python').exists())

    def test_education_view(self):
        response = self.client.get(reverse('education'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/education.html')
        self.assertTrue(Education.objects.filter(degree__icontains='MCA').exists())

    def test_contact_view_get(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/contact.html')
        self.assertIn('form', response.context)

    def test_contact_view_post_valid(self):
        data = {
            'name': 'Test Recruiter',
            'email': 'recruiter@techcorp.com',
            'subject': 'Interview Invitation',
            'message': 'We reviewed your portfolio and would like to connect.',
            'website_url_hp': '',  # Honeypot must be empty for real users
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)
        msg = ContactMessage.objects.first()
        self.assertEqual(msg.name, 'Test Recruiter')
        self.assertEqual(msg.email, 'recruiter@techcorp.com')
        # Assert email notification dispatched
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Interview Invitation', mail.outbox[0].subject)

    def test_contact_view_post_honeypot_spam_rejected(self):
        data = {
            'name': 'Spam Bot',
            'email': 'bot@spam.com',
            'subject': 'Buy crypto',
            'message': 'Visit my spam link http://spam.com',
            'website_url_hp': 'http://spam-link.com',  # Filled by bot
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 200)
        # Message must be rejected and not saved
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_contact_view_post_invalid(self):
        data = {
            'name': 'Test Recruiter',
            'email': 'not-an-email',  # Invalid email format
            'subject': '',
            'message': '',
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_resume_download(self):
        response = self.client.get(reverse('resume_download'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')


class SEORoutesTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_robots_txt(self):
        response = self.client.get(reverse('robots_txt'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        content = response.content.decode()
        self.assertIn('User-agent: *', content)
        self.assertIn('Allow: /', content)
        self.assertIn('Disallow: /admin/', content)
        self.assertIn('Sitemap:', content)

    def test_sitemap_xml(self):
        response = self.client.get(reverse('sitemap_xml'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        content = response.content.decode()
        self.assertIn('<urlset', content)
        self.assertIn('/projects/', content)
        self.assertIn('/about/', content)

    def test_google_verify_exact_file(self):
        response = self.client.get(reverse('google_verify_file'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'google-site-verification: google8fa397fdd5fe6f13.html')

    def test_google_verify_fake_file_returns_404(self):
        response = self.client.get('/googlefake999.html')
        self.assertEqual(response.status_code, 404)


class SeedPortfolioCommandTestCase(TestCase):
    def test_superuser_provisioning(self):
        call_command('seed_portfolio')
        user = User.objects.filter(username='bhavesh').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password('admin123'))
