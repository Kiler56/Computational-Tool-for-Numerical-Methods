/**
 * i18n.js — Sistema de internacionalización client-side.
 * Carga archivos JSON con traducciones y aplica los textos
 * a todos los elementos con atributo data-i18n.
 */

const I18n = (() => {
    let currentLang = "es";
    let translations = {};

    /**
     * Inicializa i18n detectando el idioma del usuario.
     */
    async function init() {
        // Prioridad: 1) lang guardado en localStorage, 2) atributo data del body, 3) "es"
        const saved = localStorage.getItem("numcalc_lang");
        const bodyLang = document.body.dataset.userLang;
        currentLang = saved || bodyLang || "es";

        await loadLang(currentLang);
        applyTranslations();
        updateToggleUI();
    }

    /**
     * Carga el archivo JSON de traducciones.
     */
    async function loadLang(lang) {
        try {
            const resp = await fetch(`/static/i18n/${lang}.json`);
            if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
            translations = await resp.json();
            currentLang = lang;
        } catch (err) {
            console.warn(`[i18n] No se pudo cargar ${lang}.json, fallback a es`, err);
            if (lang !== "es") {
                await loadLang("es");
            }
        }
    }

    /**
     * Traduce una clave.
     */
    function t(key) {
        return translations[key] || key;
    }

    /**
     * Aplica traducciones a todos los elementos con data-i18n.
     */
    function applyTranslations() {
        document.querySelectorAll("[data-i18n]").forEach((el) => {
            const key = el.getAttribute("data-i18n");
            const translated = t(key);
            if (translated !== key) {
                // Si contiene HTML (strong, em, etc.), usar innerHTML
                if (translated.includes("<")) {
                    el.innerHTML = translated;
                } else {
                    el.textContent = translated;
                }
            }
        });

        // Aplicar a placeholders
        document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
            const key = el.getAttribute("data-i18n-placeholder");
            const translated = t(key);
            if (translated !== key) {
                el.placeholder = translated;
            }
        });

        // Aplicar a aria-labels
        document.querySelectorAll("[data-i18n-aria]").forEach((el) => {
            const key = el.getAttribute("data-i18n-aria");
            const translated = t(key);
            if (translated !== key) {
                el.setAttribute("aria-label", translated);
            }
        });

        // Actualizar lang del HTML
        document.documentElement.lang = currentLang;
    }

    /**
     * Cambia el idioma en vivo sin recargar la página.
     */
    async function setLang(lang) {
        if (lang === currentLang) return;
        localStorage.setItem("numcalc_lang", lang);
        await loadLang(lang);
        applyTranslations();
        updateToggleUI();

        // Traducir instrucciones del método si existe
        applyMethodInstructions();
    }

    /**
     * Actualiza el estado visual del toggle.
     */
    function updateToggleUI() {
        const btnEs = document.getElementById("lang-es");
        const btnEn = document.getElementById("lang-en");
        if (btnEs && btnEn) {
            btnEs.classList.toggle("active", currentLang === "es");
            btnEn.classList.toggle("active", currentLang === "en");
        }
    }

    /**
     * Si la página tiene instrucciones de método con data-i18n-instructions,
     * mostrar la versión del idioma correcto.
     */
    function applyMethodInstructions() {
        const container = document.querySelector("[data-instructions-es]");
        if (!container) return;

        const esHTML = container.getAttribute("data-instructions-es");
        const enHTML = container.getAttribute("data-instructions-en");

        container.innerHTML = currentLang === "en" ? enHTML : esHTML;
    }

    function getLang() {
        return currentLang;
    }

    return { init, t, setLang, getLang, applyTranslations };
})();

// Inicializar al cargar la página
document.addEventListener("DOMContentLoaded", () => {
    I18n.init();
});
