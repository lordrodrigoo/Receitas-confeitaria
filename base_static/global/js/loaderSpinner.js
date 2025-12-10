// Modular loader spinner utility
// Usage: LoaderSpinner.show(); LoaderSpinner.hide();


const LoaderSpinner = (function() {
    const loaderId = 'global-loader-spinner';
    const loaderHtml = `
      <div class="loader-spinner-overlay">
        <div class="loader-spinner"></div>
      </div>
    `;

    function show() {
        let el = document.getElementById(loaderId);
        if (!el) {
            el = document.createElement('div');
            el.id = loaderId;
            document.body.appendChild(el);
        }
        el.innerHTML = loaderHtml;
        el.style.display = 'block';
    }

    function hide() {
        const el = document.getElementById(loaderId);
        if (el) {
            el.innerHTML = '';
            el.style.display = 'none';
        }
    }

    return { show, hide };
})();

// Optional: auto-hide on page load (in case left open)
window.addEventListener('DOMContentLoaded', LoaderSpinner.hide);