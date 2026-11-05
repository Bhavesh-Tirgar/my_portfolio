# Bhavesh Tirgar — Developer Portfolio

A modern, high-performance portfolio website built with Python & Django, inspired by the "A Designer Portfolio mk1" design system. Features an ambient pastel mesh aura, 3D Memoji avatar, Bento grids, and full dynamic CMS control through the Django Admin.

---

## Live Demo & Features

- **Aesthetic Hero Section**: Signature ambient pastel gradient aura with 3D Memoji illustration.
- **Dynamic Projects Showcase**: Spotlight Vision-style showcase card + dynamic bento grid for team & solo projects.
- **Skills & Tools Bento Grid**: Category level meters + macOS/iOS-style squircle app cards.
- **Experience & Education**: Wide scenic cards + isometric 3D journey map.
- **Interactive Contact Form**: Integrated with Django database storage and messaging.
- **Full Django Admin CMS**: Add, edit, or remove skills, projects, and experiences with zero code changes.
- **Production-Ready**: Configured for Render, Railway, or Vercel with WhiteNoise static compression, Gunicorn, and environment-based security.

---

## Tech Stack

- **Backend**: Python 3, Django 6
- **Database**: SQLite (local) / PostgreSQL (production-ready via `DATABASE_URL`)
- **Frontend**: HTML5, Modern CSS, Vanilla JS, GSAP animations
- **Production Server**: Gunicorn, WhiteNoise

---

## Local Development Setup

1. **Activate virtual environment**:
   ```powershell
   venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Seed portfolio data**:
   ```bash
   python manage.py seed_portfolio
   ```

5. **Start development server**:
   ```bash
   python manage.py runserver
   ```
   Open `http://127.0.0.1:8000/` in your browser.

---

## How to Easily Add New Projects, Skills & Experience

You can manage all portfolio content directly via the Django Admin panel:

1. Visit `http://127.0.0.1:8000/admin/` (or your live production URL `/admin/`).
2. Log in with your admin credentials.
3. **To add a new Project**:
   - Click **Projects** → **Add Project**.
   - Enter Title, Summary, Description, Technologies (comma-separated), and GitHub URL.
   - Check **Featured** if you want it highlighted. Click **Save**.
4. **To add a new Skill / Tool**:
   - Click **Skills** → **Add Skill**.
   - Enter Skill Name, Category (Language, Backend, Frontend, Database, AI, Tools), and proficiency. Click **Save**.
5. **To add an Experience or Degree**:
   - Click **Experiences** or **Education** → **Add**, fill in the details, and click **Save**.

Your new items will immediately appear on the website without restarting the server!

---

## Deployment to Render (Recommended)

This repository includes a pre-configured `render.yaml` and `Procfile`:

1. Push your repository to GitHub:
   ```bash
   git add .
   git commit -m "Deploy modern portfolio website"
   git branch -M main
   git remote add origin https://github.com/Bhavesh-Tirgar/<repo-name>.git
   git push -u origin main
   ```

2. Go to [Render.com](https://render.com) and click **New → Blueprint** (or **New → Web Service**).
3. Connect your GitHub repository.
4. Render will automatically detect `render.yaml` and run:
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py seed_portfolio && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
5. Your portfolio is now live on `https://<your-app>.onrender.com`!

---

## Contact & Links

- **Email**: tirgarbhavesh2005@gmail.com
- **Phone**: +91 9313865016
- **GitHub**: [github.com/Bhavesh-Tirgar](https://github.com/Bhavesh-Tirgar)
- **LinkedIn**: [linkedin.com/in/bhavesh-tirgar-1734b4286](https://in.linkedin.com/in/bhavesh-tirgar-1734b4286)
