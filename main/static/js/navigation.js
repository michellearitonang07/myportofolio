/* Keep homepage section pills in sync with anchors and ordinary scrolling.
   Other pages retain Django's server-rendered aria-current="page" state. */
(() => {
    const nav = document.querySelector('.nav-links');
    const profile = document.getElementById('profile');
    if (!nav || !profile) return;
    const links = [...nav.querySelectorAll('a')];
    const sectionLinks = new Map();
    for (const link of links) {
        const url = new URL(link.href);
        if (url.origin !== location.origin || url.pathname !== location.pathname) continue;
        sectionLinks.set(url.hash.slice(1) || 'profile', link);
    }
    const sections = [...document.querySelectorAll('main section[id]')];
    function update() {
        const header = document.querySelector('.site-header');
        const anchorOffset = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 0;
        const headerOffset = getComputedStyle(header).position === 'sticky' ? header.offsetHeight : 0;
        const offset = Math.max(anchorOffset, headerOffset) + 24;
        let current = profile;
        for (const section of sections) {
            if (section.getBoundingClientRect().top <= offset) current = section;
        }
        for (const link of sectionLinks.values()) link.removeAttribute('aria-current');
        const active = sectionLinks.get(current.id);
        if (active) active.setAttribute('aria-current', current === profile ? 'page' : 'location');
    }
    let scheduled = false;
    function scheduleUpdate() {
        if (scheduled) return;
        scheduled = true;
        requestAnimationFrame(() => { scheduled = false; update(); });
    }
    addEventListener('scroll', scheduleUpdate, { passive: true });
    addEventListener('resize', scheduleUpdate);
    addEventListener('hashchange', scheduleUpdate);
    addEventListener('load', scheduleUpdate);
    update();
})();
