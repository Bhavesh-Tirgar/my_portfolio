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
                const headerOffset = 80;
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
});
