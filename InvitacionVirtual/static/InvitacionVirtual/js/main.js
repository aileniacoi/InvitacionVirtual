/* ============================================================
   main.js — Animaciones cinematográficas premium
   ============================================================ */

// --- Smooth scroll para anchor links ---
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
});

// --- Auto-hide mensajes Django ---
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.message').forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            msg.style.opacity = '0';
            msg.style.transform = 'translateX(420px)';
            setTimeout(() => msg.remove(), 500);
        }, 5000);
    });
});

// ============================================================
// REVEAL ON SCROLL — IntersectionObserver premium
// ============================================================
document.addEventListener('DOMContentLoaded', function () {

    // Elementos con .reveal (fade-up individual)
    const revealObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.willChange = 'opacity, transform';
                    entry.target.classList.add('is-visible');
                    // Liberar will-change después de que termina la transición
                    entry.target.addEventListener('transitionend', () => {
                        entry.target.style.willChange = 'auto';
                    }, { once: true });
                    revealObserver.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.12, rootMargin: '0px 0px -60px 0px' }
    );

    document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

    // Elementos con .reveal-stagger (stagger en hijos — countdown, etc.)
    const staggerObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    staggerObserver.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
    );

    document.querySelectorAll('.reveal-stagger').forEach(el => staggerObserver.observe(el));
});

// ============================================================
// PARALLAX HERO — transform: translateY (GPU-composited, sin repaint)
// ============================================================
const heroImg = document.querySelector('.hero-bg');
if (heroImg && window.matchMedia('(min-width: 769px)').matches) {
    heroImg.style.willChange = 'transform';
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(() => {
                const scrolled = window.pageYOffset;
                // translateY en vez de background-position: composited por la GPU, cero repaint
                // factor 0.22 = efecto muy sutil; scale(1.06) en CSS garantiza sin bordes
                const drift = scrolled * 0.22;
                heroImg.style.transform = `scale(1.06) translateY(${drift}px)`;
                ticking = false;
            });
            ticking = true;
        }
    }, { passive: true });
}

