# Roadmap: Bhavesh Tirgar Portfolio (Production & Scalability)

This roadmap follows the **GSD (Get Shit Done)** framework and autonomous engineering lifecycle to maintain architectural stability and test-verified deliveries.

---

## Milestones

- [x] **Milestone 1: Modern UI & Aesthetic Redesign**
  - Redesign UI matching Figma *A Designer Portfolio mk1* (French chic, 3D Memoji, squircle bento grid).
  - Convert all templates to English.
  - Filter projects to the 5 verified repositories.

- [x] **Milestone 2: Production Readiness & Render Cloud Deployment**
  - Configure WhiteNoise for zero-maintenance asset compression.
  - Automate superuser auto-provisioning (`bhavesh` / `admin123`) without shell dependency.
  - Push repository to GitHub (`Bhavesh-Tirgar/my_portfolio`) with Render Auto-Deploy on commit.

- [x] **Milestone 3: Google SEO & Search Console Integration**
  - Technical SEO: dynamic `robots.txt` and `sitemap.xml`.
  - JSON-LD Schema.org structured data (`Person` entity).
  - Google Search Console ownership verification & priority crawl queue request.

- [ ] **Milestone 4: Test Safety Net & Backpressure (Current)**
  - [x] Set up GSD structure (`.planning/ROADMAP.md`, `.planning/STATE.md`).
  - [ ] Write isolated unit tests for all public endpoints (`home`, `about`, `projects`, `skills`, `education`, `contact`).
  - [ ] Write integration tests for Contact Message submissions and persistence.
  - [ ] Write tests for SEO routes (`robots.txt`, `sitemap.xml`, anti-cloaking 404s).
  - [ ] Verify test backpressure (`manage.py test` passes 100%).

- [ ] **Milestone 5: Production Enhancements**
  - [ ] Real-time email notification dispatcher on contact form submissions (SMTP / SendGrid).
  - [ ] Persistent cloud database connection (Render PostgreSQL / Neon) for zero-loss redeploys.
