from django.db import models


class Profile(models.Model):
    full_name = models.CharField(max_length=120, default='Bhavesh Tirgar')
    headline = models.CharField(max_length=200, default='MCA Student | Python & Django Developer')
    short_bio = models.TextField(default='I am a software development student focused on building practical projects with Python, Django, and modern web technologies.')
    email = models.EmailField(blank=True, default='bhavesh@example.com')
    phone = models.CharField(max_length=30, blank=True, default='')
    location = models.CharField(max_length=120, default='Gujarat, India')
    github_url = models.URLField(blank=True, default='https://github.com/')
    linkedin_url = models.URLField(blank=True, default='https://in.linkedin.com/in/bhavesh-tirgar-1734b4286')
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'

    def __str__(self):
        return self.full_name


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('Language', 'Language'),
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Database', 'Database'),
        ('AI', 'AI'),
        ('Tools', 'Tools'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Language')
    proficiency = models.PositiveIntegerField(default=80)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['category', 'order', 'name']

    def __str__(self):
        return self.name


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    is_current = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-is_current', 'order', 'period']

    def __str__(self):
        return f'{self.degree} - {self.institution}'


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.CharField(max_length=250)
    description = models.TextField()
    technologies = models.TextField(help_text='Comma separated technologies used in the project.')
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['featured', 'order', 'title']

    def __str__(self):
        return self.title

    @property
    def tech_list(self):
        return [item.strip() for item in self.technologies.split(',') if item.strip()]


class Experience(models.Model):
    TYPE_CHOICES = [
        ('Internship', 'Internship'),
        ('Professional', 'Professional'),
        ('Academic', 'Academic'),
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    period = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Internship')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'period']

    def __str__(self):
        return f'{self.title} - {self.company}'


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name}: {self.subject}'
