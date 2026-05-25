/**
 * Sidebar: collapsible method categories + live search filter.
 */
const SidebarNav = (() => {
    const STORAGE_KEY = 'numcalc_nav_expanded';
    const DEFAULT_EXPANDED = {
        linear_system: true,
        interpolation: false,
        root: false,
    };

    let searchInput;
    let clearBtn;
    let noResultsEl;
    let groups;

    function normalize(text) {
        return (text || '')
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '');
    }

    function getExpandedState() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (raw) return { ...DEFAULT_EXPANDED, ...JSON.parse(raw) };
        } catch (_) { /* ignore */ }
        return { ...DEFAULT_EXPANDED };
    }

    function saveExpandedState() {
        const state = {};
        groups.forEach((group) => {
            const cat = group.dataset.category;
            if (cat) state[cat] = group.classList.contains('is-expanded');
        });
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    }

    function setGroupExpanded(group, expanded) {
        group.classList.toggle('is-expanded', expanded);
        const toggle = group.querySelector('.nav-group-toggle');
        if (toggle) toggle.setAttribute('aria-expanded', expanded ? 'true' : 'false');
    }

    function applyExpandedDefaults() {
        const saved = getExpandedState();
        groups.forEach((group) => {
            const cat = group.dataset.category;
            const expanded = saved[cat] !== undefined ? saved[cat] : true;
            setGroupExpanded(group, expanded);
        });
    }

    function expandGroupForActiveLink() {
        const active = document.querySelector('.nav-group-panel .nav-link.active');
        if (!active) return;
        const group = active.closest('.nav-group');
        if (group) setGroupExpanded(group, true);
    }

    function updateGroupCounts() {
        groups.forEach((group) => {
            const countEl = group.querySelector('.nav-group-count');
            if (!countEl) return;
            const visible = group.querySelectorAll('.nav-item:not(.is-filtered)').length;
            const total = group.querySelectorAll('.nav-item').length;
            countEl.textContent = `(${visible}${visible !== total ? `/${total}` : ''})`;
            countEl.style.display = total ? '' : 'none';
        });
    }

    function filterMethods(query) {
        const q = normalize(query.trim());
        const tokens = q ? q.split(/\s+/).filter(Boolean) : [];
        let anyVisible = false;

        groups.forEach((group) => {
            let groupHasMatch = false;
            group.querySelectorAll('.nav-item').forEach((item) => {
                const haystack = normalize(item.dataset.search || '');
                const match = tokens.length === 0 || tokens.every((t) => haystack.includes(t));
                item.classList.toggle('is-filtered', !match);
                if (match) groupHasMatch = true;
            });

            if (tokens.length > 0) {
                setGroupExpanded(group, groupHasMatch);
                group.classList.toggle('is-empty', !groupHasMatch);
            } else {
                group.classList.remove('is-empty');
            }

            if (groupHasMatch) anyVisible = true;
        });

        if (noResultsEl) {
            noResultsEl.classList.toggle('is-visible', tokens.length > 0 && !anyVisible);
        }

        updateGroupCounts();
    }

    function bindSearch() {
        if (!searchInput) return;

        const onSearch = () => {
            filterMethods(searchInput.value);
            if (clearBtn) {
                clearBtn.classList.toggle('is-visible', searchInput.value.length > 0);
            }
        };

        searchInput.addEventListener('input', onSearch);
        searchInput.addEventListener('search', onSearch);

        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                searchInput.value = '';
                searchInput.focus();
                applyExpandedDefaults();
                onSearch();
            });
        }
    }

    function bindToggles() {
        groups.forEach((group) => {
            const toggle = group.querySelector('.nav-group-toggle');
            if (!toggle) return;
            toggle.addEventListener('click', () => {
                const expanded = !group.classList.contains('is-expanded');
                setGroupExpanded(group, expanded);
                saveExpandedState();
            });
        });
    }

    function highlightActive() {
        const currentPath = window.location.pathname;
        document.querySelectorAll('.nav-group-panel .nav-link').forEach((link) => {
            link.classList.toggle('active', link.getAttribute('href') === currentPath);
        });
        expandGroupForActiveLink();
    }

    function hideEmptyGroups() {
        groups.forEach((group) => {
            const hasItems = group.querySelectorAll('.nav-item').length > 0;
            group.style.display = hasItems ? '' : 'none';
        });
    }

    function init() {
        searchInput = document.getElementById('method-search');
        clearBtn = document.getElementById('method-search-clear');
        noResultsEl = document.getElementById('nav-no-results');
        groups = document.querySelectorAll('.nav-group');

        if (!groups.length) return;

        hideEmptyGroups();
        applyExpandedDefaults();
        bindToggles();
        bindSearch();
        highlightActive();
        updateGroupCounts();

        document.addEventListener('numcalc:langchange', () => {
            if (typeof I18n !== 'undefined') I18n.applyTranslations();
        });
    }

    return { init, filterMethods, highlightActive };
})();

document.addEventListener('DOMContentLoaded', () => SidebarNav.init());
