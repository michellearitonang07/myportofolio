/* Daftar Experience: teks API selalu dirender melalui DOM, bukan innerHTML. */
(() => {
    const page = document.getElementById('experience');
    if (!page) return;
    const search = document.getElementById('experience-search');
    const searchForm = document.getElementById('experience-search-form');
    const grid = document.getElementById('experience-grid');
    const results = document.getElementById('experience-results');
    const states = ['loading', 'error', 'empty', 'grid'];
    const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
    const dummyUUID = '00000000-0000-0000-0000-000000000000';
    let controller;
    let searchTimer;

    function element(tag, className, text) {
        const node = document.createElement(tag);
        node.className = className;
        if (text !== undefined) node.textContent = text;
        return node;
    }

    function displayState(state) {
        states.forEach(name => document.getElementById(`experience-${name}`).classList.toggle('hide', name !== state));
        results.setAttribute('aria-busy', String(state === 'loading'));
    }

    function postForm(url, className) {
        const form = element('form', className);
        form.method = 'post';
        form.action = url;
        form.append(document.getElementById('experience-csrf-token').content.firstElementChild.cloneNode(true));
        return form;
    }

    function dateText(value) {
        return new Intl.DateTimeFormat('id-ID', {dateStyle: 'medium', timeZone: 'Asia/Jakarta'}).format(new Date(value));
    }

    function buildCard(item) {
        const fields = item?.fields;
        if (typeof item?.pk !== 'string' || !uuidPattern.test(item.pk) || !fields ||
            !['title', 'description', 'category', 'category_label', 'started_at'].every(key => typeof fields[key] === 'string') ||
            !Number.isFinite(Date.parse(fields.started_at)) ||
            !(fields.ended_at === null || (typeof fields.ended_at === 'string' && Number.isFinite(Date.parse(fields.ended_at)))) ||
            !(fields.thumbnail === null || typeof fields.thumbnail === 'string') ||
            typeof fields.is_ongoing !== 'boolean' || typeof fields.is_starred !== 'boolean' ||
            !Number.isSafeInteger(fields.star_count) || fields.star_count < 0) {
            throw new Error('Format data pengalaman tidak valid.');
        }
        const article = element('article', 'experience-card');
        article.dataset.experienceId = item.pk;
        const body = element('div', 'experience-card__body');
        if (fields.thumbnail) {
            try {
                const url = new URL(fields.thumbnail);
                if (['http:', 'https:'].includes(url.protocol) && !url.username && !url.password) {
                    const image = element('img', 'experience-thumbnail');
                    image.alt = `Gambar pengalaman: ${fields.title}`;
                    image.loading = 'lazy';
                    image.referrerPolicy = 'no-referrer';
                    image.addEventListener('error', () => image.remove(), {once: true});
                    image.src = url.href;
                    body.append(image);
                }
            } catch (_) { /* URL gambar lama yang tidak valid tidak menghalangi kartu lain. */ }
        }
        body.append(element('span', 'experience-category', fields.category_label));
        body.append(element('h2', '', fields.title));
        body.append(element('p', 'experience-description', fields.description));
        body.append(element('p', 'experience-status' + (fields.is_ongoing ? ' is-ongoing' : ''), fields.is_ongoing ? 'Sedang berlangsung' : 'Selesai'));
        // started_at merupakan waktu pencatatan otomatis, bukan tanggal mulai kegiatan.
        const dates = element('p', 'experience-dates', `Dicatat ${dateText(fields.started_at)}`);
        if (fields.ended_at) dates.append(document.createTextNode(` · Selesai ${dateText(fields.ended_at)}`));
        body.append(dates);
        const actions = element('div', 'card-actions');
        const starForm = postForm(page.dataset.starUrl.replace(dummyUUID, item.pk), 'star-form');
        const starButton = element('button', 'button button-star' + (fields.is_starred ? ' is-starred' : ''), fields.is_starred ? '★ Batal bintang ' : '☆ Beri bintang ');
        starButton.type = 'submit';
        starButton.setAttribute('aria-pressed', String(fields.is_starred));
        starButton.setAttribute('aria-label', `${fields.is_starred ? 'Batalkan bintang untuk' : 'Beri bintang untuk'} ${fields.title}`);
        starButton.append(element('span', 'star-count', fields.star_count));
        starForm.append(starButton);
        actions.append(starForm);
        if (page.dataset.canEdit === 'true') {
            const edit = element('a', 'btn btn-outline experience-edit', 'Ubah');
            edit.href = page.dataset.editUrl.replace(dummyUUID, item.pk);
            actions.append(edit);
        }
        if (page.dataset.canDelete === 'true') {
            const form = postForm(page.dataset.deleteUrl.replace(dummyUUID, item.pk), 'experience-delete-form');
            const button = element('button', 'btn btn-danger', 'Hapus');
            button.type = 'submit';
            form.append(button);
            form.addEventListener('submit', event => {
                if (!confirm('Apakah kamu yakin ingin menghapus pengalaman ini?')) event.preventDefault();
            });
            actions.append(form);
        }
        article.append(body, actions);
        return article;
    }

    async function fetchExperiences() {
        controller?.abort();
        const activeController = new AbortController();
        controller = activeController;
        const query = search.value.trim();
        displayState('loading');
        try {
            const url = new URL(page.dataset.listUrl, location.origin);
            if (query) url.searchParams.set('title', query);
            const response = await fetch(url, {headers: {'Accept': 'application/json'}, signal: activeController.signal});
            if (!response.ok) throw new Error('Server belum dapat mengirim data pengalaman.');
            const data = await response.json();
            if (activeController.signal.aborted || controller !== activeController) return;
            if (!Array.isArray(data)) throw new Error('Respons server bukan daftar pengalaman.');
            const cards = data.map(buildCard);
            grid.replaceChildren(...cards);
            document.querySelector('#experience-empty p').textContent = query
                ? 'Tidak ada pengalaman dengan judul tersebut.' : 'Belum ada pengalaman yang ditambahkan.';
            displayState(cards.length ? 'grid' : 'empty');
        } catch (_) {
            // Respons maupun kegagalan permintaan lama tidak boleh menimpa pencarian terbaru.
            if (activeController.signal.aborted || controller !== activeController) return;
            displayState('error');
            showToast('Gagal memuat pengalaman', 'Periksa koneksi atau coba lagi beberapa saat.', 'error');
        }
    }

    search.addEventListener('input', () => {
        clearTimeout(searchTimer);
        controller?.abort();
        searchTimer = setTimeout(fetchExperiences, 300);
    });
    searchForm.addEventListener('submit', event => {
        event.preventDefault();
        clearTimeout(searchTimer);
        fetchExperiences();
    });
    document.getElementById('retry-experience').addEventListener('click', () => {
        clearTimeout(searchTimer);
        fetchExperiences();
    });
    const modal = document.getElementById('add-experience-modal');
    const form = document.getElementById('experience-form');
    if (modal && form) {
        const opener = document.querySelector('.experience-add-button');
        const summary = document.getElementById('experience-form-errors');
        const submitButton = form.querySelector('button[type="submit"]');
        const fieldset = form.querySelector('fieldset');
        const fieldNames = ['title', 'description', 'category', 'thumbnail', 'ended_at'];
        const previousInert = new Map();
        let submitting = false;
        for (const name of fieldNames) {
            const input = form.elements.namedItem(name);
            const help = document.getElementById(`${input.id}_help`);
            input.setAttribute('aria-describedby', `${input.id}_errors${help ? ` ${help.id}` : ''}`);
        }
        modal.addEventListener('toggle', event => {
            if (event.newState === 'open') {
                document.querySelectorAll('header, main, footer').forEach(node => {
                    previousInert.set(node, node.inert);
                    node.inert = true;
                });
                if (submitting) modal.querySelector('.project-form-modal__close').focus();
                else form.elements.namedItem('title').focus();
            } else {
                previousInert.forEach((value, node) => { node.inert = value; });
                previousInert.clear();
                opener.focus();
            }
        });
        modal.addEventListener('keydown', event => {
            if (event.key !== 'Tab') return;
            const controls = [...modal.querySelectorAll('.project-form-modal__content button, input:not([type="hidden"]), textarea, select')]
                .filter(node => !node.matches(':disabled'));
            const first = controls[0];
            const last = controls[controls.length - 1];
            if (event.shiftKey && document.activeElement === first) {
                event.preventDefault();
                last.focus();
            } else if (!event.shiftKey && document.activeElement === last) {
                event.preventDefault();
                first.focus();
            }
        });

        function clearErrors() {
            summary.replaceChildren();
            form.querySelectorAll('[data-field-errors]').forEach(node => node.replaceChildren());
            fieldNames.forEach(name => form.elements.namedItem(name).removeAttribute('aria-invalid'));
        }

        function displayErrors(errors, fallback) {
            const messages = [];
            if (errors && typeof errors === 'object' && !Array.isArray(errors)) {
                for (const [name, entries] of Object.entries(errors)) {
                    if (!Array.isArray(entries)) continue;
                    for (const error of entries) {
                        if (typeof error?.message !== 'string') continue;
                        messages.push(error.message);
                        if (fieldNames.includes(name)) {
                            const input = form.elements.namedItem(name);
                            input.setAttribute('aria-invalid', 'true');
                            document.getElementById(`${input.id}_errors`).append(element('li', '', error.message));
                        }
                    }
                }
            }
            summary.textContent = messages.length ? messages.join(' ') : fallback;
            showToast('Gagal menambahkan pengalaman', summary.textContent, 'error', 6000);
        }

        form.addEventListener('submit', async event => {
            event.preventDefault();
            if (submitting) return;
            submitting = true;
            clearErrors();
            // Ambil FormData sebelum fieldset dinonaktifkan agar seluruh isian dan CSRF ikut dikirim.
            const body = new FormData(form);
            fieldset.disabled = true;
            submitButton.disabled = true;
            submitButton.textContent = 'Menyimpan...';
            form.setAttribute('aria-busy', 'true');
            let failed = false;
            try {
                const response = await fetch(form.dataset.createUrl, {
                    method: 'POST', headers: {'Accept': 'application/json'}, body,
                });
                const result = await response.json().catch(() => null);
                if (response.status === 201 && typeof result?.pk === 'string' && uuidPattern.test(result.pk)) {
                    form.reset();
                    modal.hidePopover();
                    showToast('Berhasil', 'Pengalaman berhasil ditambahkan. Daftar diperbarui sesuai pencarian aktif.', 'success');
                    clearTimeout(searchTimer);
                    await fetchExperiences();
                } else {
                    failed = true;
                    const fallback = response.status === 403
                        ? 'Akses ditolak atau sesi/token CSRF tidak berlaku. Muat ulang halaman dan masuk dengan akun yang berhak.'
                        : 'Respons server tidak sesuai. Periksa daftar sebelum mencoba menyimpan kembali.';
                    displayErrors(result?.errors, typeof result?.message === 'string' ? result.message : fallback);
                }
            } catch (_) {
                failed = true;
                displayErrors(null, 'Koneksi terputus. Isian tetap tersimpan di form. Periksa daftar sebelum mencoba lagi agar data tidak terduplikasi.');
            } finally {
                submitting = false;
                fieldset.disabled = false;
                submitButton.disabled = false;
                submitButton.textContent = 'Simpan Pengalaman';
                form.setAttribute('aria-busy', 'false');
                if (failed && modal.matches(':popover-open')) {
                    const invalid = form.querySelector('[aria-invalid="true"]');
                    (invalid || summary).focus();
                }
            }
        });
    }
    fetchExperiences();
})();
