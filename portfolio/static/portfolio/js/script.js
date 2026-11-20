/**
 * A DESIGNER PORTFOLIO MK1 - CLIENT SCRIPT
 * Theme Switcher, Smooth Scrolling & Fluid Micro-Interactions (English)
 */

document.addEventListener('DOMContentLoaded', function () {
    // 1. Current Year in Footer
    const yearNode = document.getElementById('year');
    if (yearNode) {
        yearNode.textContent = new Date().getFullYear();
    }

    // 2. Theme Toggle (Light / Dark Mode)
    const themeToggleBtn = document.getElementById('theme-toggle');
    const rootHtml = document.documentElement;
    const storedTheme = localStorage.getItem('designer_theme');

    // Default to light (as in the Figma design) unless user previously chose dark
    if (storedTheme === 'dark') {
        rootHtml.setAttribute('data-theme', 'dark');
    } else {
        rootHtml.setAttribute('data-theme', 'light');
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', function () {
            const currentTheme = rootHtml.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            rootHtml.setAttribute('data-theme', newTheme);
            localStorage.setItem('designer_theme', newTheme);
        });
    }

    // 3. Mobile Menu Drawer Toggle
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const mobileDrawer = document.getElementById('mobile-drawer');

    if (mobileMenuToggle && mobileDrawer) {
        mobileMenuToggle.addEventListener('click', function () {
            mobileDrawer.classList.toggle('open');
        });

        const mobileLinks = mobileDrawer.querySelectorAll('.mobile-nav-link');
        mobileLinks.forEach(function (link) {
            link.addEventListener('click', function () {
                mobileDrawer.classList.remove('open');
            });
        });
    }

    // 4. Smooth Anchor Scrolling with Header Offset
    document.querySelectorAll('a[href*="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            const targetId = href.substring(href.indexOf('#') + 1);
            if (!targetId) return;

            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                e.preventDefault();
                const headerOffset = 96;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });

                if (history.pushState) {
                    history.pushState(null, null, '#' + targetId);
                }
            }
        });
    });

    // 5. Active Nav Highlighting on Scroll
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.desktop-nav .nav-item');

    function highlightNavOnScroll() {
        const scrollPosition = window.scrollY + 120;

        sections.forEach(function (section) {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute('id');

            if (scrollPosition >= top && scrollPosition < top + height) {
                navLinks.forEach(function (link) {
                    link.classList.remove('active');
                    if (link.getAttribute('href').includes('#' + id)) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }

    window.addEventListener('scroll', highlightNavOnScroll, { passive: true });

    // 6. Micro-Interactions via GSAP (if available)
    if (window.gsap) {
        gsap.from('.hero-copy-column', {
            opacity: 0,
            y: 20,
            duration: 0.9,
            ease: 'power2.out'
        });

        gsap.from('.hero-visual-column', {
            opacity: 0,
            scale: 0.96,
            duration: 1,
            delay: 0.15,
            ease: 'power2.out'
        });
    }

    // 7. MotionSites & React Bits: Spotlight, 3D Gyroscopic Tilt & Magnetic Buttons
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const isFinePointer = window.matchMedia('(pointer: fine)').matches;

    if (!prefersReducedMotion) {
        // A. Spotlight Cursor Follower (Cards & Tiles)
        const spotlightCards = document.querySelectorAll(
            '.spotlight-card, .project-spotlight-card, .tech-project-card, .app-tile'
        );

        spotlightCards.forEach(function (card) {
            card.addEventListener('mousemove', function (e) {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);
                card.style.setProperty('--spotlight-opacity', '1');
            });

            card.addEventListener('mouseleave', function () {
                card.style.setProperty('--spotlight-opacity', '0');
            });
        });

        // B. React Bits: 3D Parallax Tilt (Desktop / Fine pointer)
        if (isFinePointer) {
            const tiltCards = document.querySelectorAll(
                '.tilt-card, .project-spotlight-card, .tech-project-card'
            );

            tiltCards.forEach(function (card) {
                card.addEventListener('mousemove', function (e) {
                    const rect = card.getBoundingClientRect();
                    const x = (e.clientX - rect.left) / rect.width;
                    const y = (e.clientY - rect.top) / rect.height;
                    const maxTilt = 4.5;
                    const rotateX = ((0.5 - y) * (maxTilt * 2)).toFixed(2);
                    const rotateY = ((x - 0.5) * (maxTilt * 2)).toFixed(2);
                    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-2px)`;
                });

                card.addEventListener('mouseleave', function () {
                    card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)';
                });
            });

            // C. React Bits: Magnetic Button Pull
            const magneticButtons = document.querySelectorAll('.btn-magnetic, .btn-pill');

            magneticButtons.forEach(function (btn) {
                btn.addEventListener('mousemove', function (e) {
                    const rect = btn.getBoundingClientRect();
                    const centerX = rect.left + rect.width / 2;
                    const centerY = rect.top + rect.height / 2;
                    const deltaX = (e.clientX - centerX) * 0.22;
                    const deltaY = (e.clientY - centerY) * 0.22;
                    btn.style.transform = `translate(${deltaX.toFixed(1)}px, ${deltaY.toFixed(1)}px)`;
                });

                btn.addEventListener('mouseleave', function () {
                    btn.style.transform = '';
                });
            });
        }
    }
});
