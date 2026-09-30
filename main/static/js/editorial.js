/* Progressive enhancement: content stays visible without JS or reduced motion. */
(() => {
    const reduced = matchMedia('(prefers-reduced-motion: reduce)');
    const strip = document.querySelector('.editorial-strip');
    const toggle = document.querySelector('.marquee-toggle');
    if (strip && toggle) {
        toggle.hidden = false;
        toggle.addEventListener('click', () => {
            const paused = strip.classList.toggle('is-paused');
            toggle.setAttribute('aria-pressed', String(paused));
            toggle.textContent = paused ? 'Resume motion' : 'Pause motion';
        });
    }
    if (!('IntersectionObserver' in window)) return;
    const cards = [...document.querySelectorAll('.about-layout > div, .journey-layout > div, .currently-grid article, .education-card, .skill-category, .memory-card')];
    const observer = new IntersectionObserver(entries => {
        for (const entry of entries) {
            if (entry.isIntersecting) {
                entry.target.classList.remove('reveal-pending');
                observer.unobserve(entry.target);
            }
        }
    }, { threshold: 0.06 });
    function configure() {
        observer.disconnect();
        cards.forEach((card, index) => {
            card.classList.remove('reveal-pending');
            if (!reduced.matches && card.getBoundingClientRect().top > innerHeight) {
                card.style.setProperty('--reveal-delay', `${index % 3 * 55}ms`);
                card.classList.add('reveal-pending');
                observer.observe(card);
            }
        });
    }
    reduced.addEventListener('change', configure);
    configure();
})();
