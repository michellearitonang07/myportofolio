let toastTimer;

function showToast(title, message, type = 'normal', duration = 3000) {
    const component = document.getElementById('toast-component');
    const titleElement = document.getElementById('toast-title');
    const messageElement = document.getElementById('toast-message');
    if (!component || !titleElement || !messageElement) return;

    clearTimeout(toastTimer);
    component.classList.remove('toast-success', 'toast-error', 'toast-normal');
    const toastType = ['success', 'error'].includes(type) ? type : 'normal';
    component.classList.add(`toast-${toastType}`);
    titleElement.textContent = title;
    messageElement.textContent = message;

    if (!component.matches(':popover-open')) {
        component.showPopover();
        void component.offsetHeight; // Start the transition from the hidden position.
    }
    component.classList.remove('toast-hidden');
    component.classList.add('toast-show');

    toastTimer = setTimeout(() => {
        component.classList.remove('toast-show');
        component.classList.add('toast-hidden');
        // Reuse the timer so a new notification also cancels a pending exit.
        toastTimer = setTimeout(() => component.hidePopover(), 300);
    }, duration);
}
