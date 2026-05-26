/**
 * steps.js — Render intermediate steps.
 */

let globalSteps = [];
let currentStepIndex = 0;
let currentViewMode = 'all'; // 'all' or 'step'

/**
 * Limpia pasos, tablas y estado del visor paso a paso (p. ej. tras un error).
 */
function resetStepsState() {
    globalSteps = [];
    currentStepIndex = 0;
    currentViewMode = 'all';

    const container = document.getElementById('steps-container');
    if (container) container.innerHTML = '';

    const stepControls = document.getElementById('step-controls');
    if (stepControls) stepControls.style.display = 'none';

    const btnViewAll = document.getElementById('btn-view-all');
    const btnViewStep = document.getElementById('btn-view-step');
    if (btnViewAll) btnViewAll.classList.add('active');
    if (btnViewStep) btnViewStep.classList.remove('active');
}

/**
 * Renderiza la lista de pasos dentro del contenedor indicado.
 */
function renderSteps(steps, containerId) {
    globalSteps = steps;
    currentStepIndex = 0;
    updateStepsView(containerId);
}

function updateStepsView(containerId = 'steps-container') {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = '';
    
    const stepControls = document.getElementById('step-controls');
    const btnViewAll = document.getElementById('btn-view-all');
    const btnViewStep = document.getElementById('btn-view-step');
    
    if (!globalSteps || globalSteps.length === 0) return;

    if (currentViewMode === 'all') {
        if (stepControls) stepControls.style.display = 'none';
        if (btnViewAll) btnViewAll.classList.add('active');
        if (btnViewStep) btnViewStep.classList.remove('active');
        
        globalSteps.forEach((step, index) => {
            container.appendChild(createStepElement(step, index));
        });
    } else {
        if (stepControls) stepControls.style.display = 'flex';
        if (btnViewAll) btnViewAll.classList.remove('active');
        if (btnViewStep) btnViewStep.classList.add('active');
        
        updateStepControls();
        container.appendChild(createStepElement(globalSteps[currentStepIndex], 0));
    }
}

function setViewMode(mode) {
    currentViewMode = mode;
    updateStepsView();
}

function nextStep() {
    if (currentStepIndex < globalSteps.length - 1) {
        currentStepIndex++;
        updateStepsView();
    }
}

function prevStep() {
    if (currentStepIndex > 0) {
        currentStepIndex--;
        updateStepsView();
    }
}

function updateStepControls() {
    const btnPrev = document.getElementById('btn-prev-step');
    const btnNext = document.getElementById('btn-next-step');
    const display = document.getElementById('current-step-display');
    
    if (btnPrev) btnPrev.disabled = (currentStepIndex === 0);
    if (btnNext) btnNext.disabled = (currentStepIndex === globalSteps.length - 1);
    const currentLang = window.I18n ? window.I18n.getLang() : 'es';
    if (display) {
        if (currentLang === 'en') {
            display.textContent = `Step ${currentStepIndex + 1} of ${globalSteps.length}`;
        } else {
            display.textContent = `Paso ${currentStepIndex + 1} de ${globalSteps.length}`;
        }
    }
}

function createStepElement(step, index) {
    const stepEl = document.createElement('div');
    stepEl.className = 'step-card';
    stepEl.style.animationDelay = `${index * 0.05}s`;

    const lang = (typeof I18n !== 'undefined') ? I18n.getLang() : 'es';

    // Encabezado del paso
    let badges = '';
    if (step.swap_rows) {
        const rowStr = lang === 'en' ? 'Rows' : 'Filas';
        badges += `<span class="badge badge-swap">↕ ${rowStr} ${step.swap_rows[0]+1} ↔ ${step.swap_rows[1]+1}</span>`;
    }
    if (step.swap_cols) {
        const colStr = lang === 'en' ? 'Cols' : 'Cols';
        badges += `<span class="badge badge-swap-col">↔ ${colStr} ${step.swap_cols[0]+1} ↔ ${step.swap_cols[1]+1}</span>`;
    }

    const phaseLabels = {
        'elimination': { es: 'Eliminación', en: 'Elimination' },
        'forward_sweep': { es: 'Barrido Hacia Adelante', en: 'Forward Sweep' },
        'back_substitution': { es: 'Sustitución Hacia Atrás', en: 'Back Substitution' },
        'forward_substitution': { es: 'Sustitución Hacia Adelante', en: 'Forward Substitution' },
        'extract': { es: 'Extracción', en: 'Extraction' },
        'reorder': { es: 'Reorden', en: 'Reordering' },
        'analysis': { es: 'Análisis', en: 'Analysis' },
        'lagrange_setup': { es: 'Configuración Lagrange', en: 'Lagrange Setup' },
        'lagrange_basis': { es: 'Base L_j', en: 'L_j Basis' },
        'lagrange_sum': { es: 'Suma de Términos', en: 'Sum of Terms' },
        'setup': { es: 'Configuración', en: 'Setup' },
        'evaluation': { es: 'Evaluación', en: 'Evaluation' },
        'weighted_sum': { es: 'Suma Ponderada', en: 'Weighted Sum' },
        'result': { es: 'RESULTADO', en: 'RESULT' },
        'error_estimation': { es: 'Estimación de Error', en: 'Error Estimation' },
        'bisection': { es: 'Bisección', en: 'Bisection' },
        'root_found': { es: 'Raíz Encontrada', en: 'Root Found' },
        'max_iter_reached': { es: 'Límite Iteraciones', en: 'Max Iterations' },
        'converged': { es: 'Convergencia', en: 'Converged' },
        'secante': { es: 'Secante', en: 'Secant' },
        'false_position': { es: 'Regla Falsa', en: 'False Position' },
        'factorization': { es: 'Factorización', en: 'Factorization' },
        'singularity': { es: 'Singularidad', en: 'Singularity' },
        'overflow': { es: 'Desbordamiento', en: 'Overflow' },
        'search': { es: 'Búsqueda', en: 'Search' }
    };

    let phaseLabel = '';
    if (step.phase && phaseLabels[step.phase]) {
        phaseLabel = phaseLabels[step.phase][lang];
    } else if (step.phase) {
        phaseLabel = step.phase.replace(/_/g, ' ').toUpperCase();
    }

    // Support bilingual descriptions
    let descText = step.description;
    if (typeof step.description === 'object' && step.description !== null) {
        descText = step.description[lang] || step.description['en'] || Object.values(step.description)[0];
    }

    stepEl.innerHTML = `
        <div class="step-header">
            <span class="step-number">${step.step}</span>
            <span class="step-phase">${phaseLabel}</span>
            ${badges}
        </div>
        <p class="step-desc">${descText}</p>
    `;

    // Renderizar la matriz del estado actual si existe
    if (step.matrix_state) {
        stepEl.appendChild(buildMatrixTable(step.matrix_state));
    }

    // Para Thomas: mostrar diagonales y RHS
    if (step.main_diagonal) {
        const info = document.createElement('div');
        info.className = 'thomas-info';
        info.innerHTML = `
            <span><strong>d:</strong> [${step.main_diagonal.map(v => v.toFixed(4)).join(', ')}]</span>
            ${step.rhs ? `<span><strong>r:</strong> [${step.rhs.map(v => v.toFixed(4)).join(', ')}]</span>` : ''}
        `;
        stepEl.appendChild(info);
    }

    return stepEl;
}

/** Build HTML table from a 2D matrix. */
function buildMatrixTable(matrix) {
    const table = document.createElement('table');
    table.className = 'matrix-table';

    matrix.forEach(row => {
        const tr = document.createElement('tr');
        row.forEach(val => {
            const td = document.createElement('td');
            td.textContent = typeof val === 'number' ? val.toFixed(4) : val;
            tr.appendChild(td);
        });
        table.appendChild(tr);
    });

    return table;
}

// Bilingual translations for dynamic backend-generated properties
const PropertyTranslations = {
    es: {
        "determinant": "Determinante",
        "strictly_diagonally_dominant": "Estrictamente Diagonal Dominante",
        "positive_definite": "Definida Positiva",
        "number_of_nodes": "Número de Nodos",
        "polynomial_degree": "Grado del Polinomio",
        "evaluated_point": "Punto Evaluado",
        "polynomial": "Polinomio",
        "coefficients_c_i": "Coeficientes c_i",
        "coefficients": "Coeficientes",
        "expanded_polynomial": "Polinomio Expandido",
        "readable_polynomial": "Polinomio Legible",
        "approximate_integral": "Integral Aproximada",
        "subintervals_used": "Subintervalos usados (n)",
        "step_h": "Paso h",
        "estimated_error": "Error estimado (Richardson)",
        "formula": "Fórmula",
        "note": "Nota",
        "spectral_radius": "Radio Espectral (ρ)",
        "convergence": "Convergencia",
        "transition_matrix_tw": "Matriz de Transición Tw",
        "transition_matrix_tj": "Matriz de Transición Tj",
        "transition_matrix_tg": "Matriz de Transición Tg",
        "matrix_l": "Matriz L:",
        "matrix_u": "Matriz U:",
        "matrix_properties": "Propiedades de la Matriz",
        "yes": "Sí",
        "no": "No",
        "guaranteed": "Garantizada (ρ < 1)",
        "not_guaranteed": "No garantizada (ρ >= 1)",
        "matrix_size": "Tamaño de la Matriz",
        "factorization": "Factorización",
        "l_diagonal": "Diagonal de L",
        "solution_vector": "Vector Solución"
    },
    en: {
        "determinant": "Determinant",
        "strictly_diagonally_dominant": "Strictly Diagonally Dominant",
        "positive_definite": "Positive Definite",
        "number_of_nodes": "Number of Nodes",
        "polynomial_degree": "Polynomial Degree",
        "evaluated_point": "Evaluated Point",
        "polynomial": "Polynomial",
        "coefficients_c_i": "Coefficients c_i",
        "coefficients": "Coefficients",
        "expanded_polynomial": "Expanded Polynomial",
        "readable_polynomial": "Readable Polynomial",
        "approximate_integral": "Approximate Integral",
        "subintervals_used": "Subintervals Used (n)",
        "step_h": "Step h",
        "estimated_error": "Estimated Error (Richardson)",
        "formula": "Formula",
        "note": "Note",
        "spectral_radius": "Spectral Radius (ρ)",
        "convergence": "Convergence",
        "transition_matrix_tw": "Transition Matrix Tw",
        "transition_matrix_tj": "Transition Matrix Tj",
        "transition_matrix_tg": "Transition Matrix Tg",
        "matrix_l": "Matrix L:",
        "matrix_u": "Matrix U:",
        "matrix_properties": "Matrix Properties",
        "yes": "Yes",
        "no": "No",
        "guaranteed": "Guaranteed (ρ < 1)",
        "not_guaranteed": "Not guaranteed (ρ >= 1)",
        "matrix_size": "Matrix size",
        "factorization": "Factorization",
        "l_diagonal": "L diagonal",
        "solution_vector": "Solution vector"
    }
};

const PropertyKeysMap = {
    "determinante": "determinant",
    "estrictamente diagonal dominante": "strictly_diagonally_dominant",
    "definida positiva": "positive_definite",
    "número de nodos": "number_of_nodes",
    "grado del polinomio": "polynomial_degree",
    "punto evaluado": "evaluated_point",
    "polinomio": "polynomial",
    "coeficientes c_i": "coefficients_c_i",
    "coeficientes": "coefficients",
    "polinomio expandido": "expanded_polynomial",
    "polinomio legible": "readable_polynomial",
    "integral aproximada": "approximate_integral",
    "subintervalos usados (n)": "subintervals_used",
    "paso h": "step_h",
    "error estimado (richardson)": "estimated_error",
    "fórmula": "formula",
    "nota": "note",
    "radio espectral (ρ)": "spectral_radius",
    "convergencia": "convergence",
    "matriz de transición tw": "transition_matrix_tw",
    "matriz de transición tj": "transition_matrix_tj",
    "matriz de transición tg": "transition_matrix_tg",
    "matrix size": "matrix_size",
    "factorization": "factorization",
    "l diagonal": "l_diagonal",
    "solution vector": "solution_vector"
};

const PropertyValuesMap = {
    "sí": "yes",
    "no": "no",
    "garantizada (ρ < 1)": "guaranteed",
    "no garantizada (ρ >= 1)": "not_guaranteed"
};

function translatePropKey(key, lang) {
    const canonical = PropertyKeysMap[key.toLowerCase().trim()];
    if (canonical && PropertyTranslations[lang] && PropertyTranslations[lang][canonical]) {
        return PropertyTranslations[lang][canonical];
    }
    const directCanonical = key.toLowerCase().replace(/\s+/g, '_');
    if (PropertyTranslations[lang] && PropertyTranslations[lang][directCanonical]) {
        return PropertyTranslations[lang][directCanonical];
    }
    return key;
}

function translatePropValue(val, lang) {
    if (typeof val !== 'string') return val;
    const canonical = PropertyValuesMap[val.toLowerCase().trim()];
    if (canonical && PropertyTranslations[lang] && PropertyTranslations[lang][canonical]) {
        return PropertyTranslations[lang][canonical];
    }
    if (val.toLowerCase().includes("n ajustado de")) {
        const match = val.match(/\d+/g);
        if (match && match.length >= 2) {
            const from = match[0];
            const to = match[1];
            if (lang === 'en') {
                return `n adjusted from ${from} to ${to} (multiple of 3)`;
            } else {
                return `n ajustado de ${from} a ${to} (múltiplo de 3)`;
            }
        }
    }
    return val;
}

/**
 * Renderiza el vector solución y propiedades de la matriz para sistemas lineales.
 */
function renderSolution(result, containerId) {
    window.currentResult = result;
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = '';
    
    const lang = (window.I18n && typeof I18n.getLang === 'function') ? I18n.getLang() : 'en';
    
    // Propiedades de la matriz
    if (result.properties) {
        const propsDiv = document.createElement('div');
        propsDiv.className = 'matrix-properties callout callout-info';
        propsDiv.style.marginBottom = '1.5rem';
        const titleText = translatePropKey("matrix_properties", lang);
        let propsHtml = `<h3 style="margin-top:0;">${titleText}</h3><ul style="margin-bottom:0;">`;
        for (const [key, value] of Object.entries(result.properties)) {
            const translatedKey = translatePropKey(key, lang);
            const translatedVal = translatePropValue(value, lang);
            let displayVal = translatedVal;
            if (typeof translatedVal === 'string' && translatedVal.includes('\n')) {
                displayVal = `<pre style="background:var(--bg-primary); padding:0.5rem; border-radius:4px; margin-top:0.25rem;">${translatedVal}</pre>`;
            }
            propsHtml += `<li style="margin-bottom:0.5rem;"><strong>${translatedKey}:</strong> ${displayVal}</li>`;
        }
        propsHtml += '</ul>';
        propsDiv.innerHTML = propsHtml;
        container.appendChild(propsDiv);
    }
    
    // Matrices L y U
    if (result.L && result.U) {
        const luDiv = document.createElement('div');
        luDiv.className = 'lu-matrices';
        luDiv.style.display = 'flex';
        luDiv.style.gap = '2rem';
        luDiv.style.marginBottom = '1.5rem';
        luDiv.style.overflowX = 'auto';
        
        const lContainer = document.createElement('div');
        const labelL = translatePropKey("matrix_l", lang);
        lContainer.innerHTML = `<h4 style="margin-bottom:0.5rem; text-align:center;">${labelL}</h4>`;
        lContainer.appendChild(buildMatrixTable(result.L));
        luDiv.appendChild(lContainer);
        
        const uContainer = document.createElement('div');
        const labelU = translatePropKey("matrix_u", lang);
        uContainer.innerHTML = `<h4 style="margin-bottom:0.5rem; text-align:center;">${labelU}</h4>`;
        uContainer.appendChild(buildMatrixTable(result.U));
        luDiv.appendChild(uContainer);
        
        container.appendChild(luDiv);
    }

    const solution = result.solution;
    if (solution && solution.length > 0) {
        const wrapper = document.createElement('div');
        wrapper.className = 'solution-vector';
        solution.forEach((val, i) => {
            const item = document.createElement('div');
            item.className = 'solution-item';
            item.innerHTML = `
                <span class="var-name">x<sub>${i + 1}</sub></span>
                <span class="var-equals">=</span>
                <span class="var-value">${val.toFixed(6)}</span>
            `;
            wrapper.appendChild(item);
        });
        container.appendChild(wrapper);
    }

    if (window.I18n && typeof I18n.applyTranslations === 'function') {
        I18n.applyTranslations();
    }
}

/**
 * Renderiza la solución de interpolación.
 */
function renderInterpSolution(result, containerId) {
    window.currentResult = result;
    const container = document.getElementById(containerId);
    if (!container) return;
    
    const lang = (window.I18n && typeof I18n.getLang === 'function') ? I18n.getLang() : 'en';
    const sol = result.solution;
    let px, xev;
    
    if (Array.isArray(sol)) {
        // Vandermonde returns coefficients
        px = result.properties["p(" + result.steps[result.steps.length - 1].eval_x + ")"] || "";
        const evStep = result.steps.find(s => s.phase === 'evaluation');
        if (evStep) {
            xev = evStep.eval_x;
            px = evStep.eval_y;
        } else {
            const el = document.getElementById('x-eval-input');
            xev = el ? el.value : '0';
            px = "See coefficients";
        }
    } else {
        px = sol.P_x !== undefined ? sol.P_x : sol.p_x;
        xev = sol.x_eval;
    }

    let px_display = typeof px === 'number' ? px.toFixed(10) : px;
    if (px === "See coefficients") {
        px_display = lang === 'en' ? "See coefficients" : "Ver coeficientes";
    }

    let polynomial =
        sol.polynomial ||
        result.properties?.["Polinomio"] ||
        "Not available";

    if (polynomial === "Not available") {
        polynomial = lang === 'en' ? "Not available" : "No disponible";
    }

    // Convert exponents to superscripts
    polynomial = polynomial
        .replace(/\*\*5/g, '⁵')
        .replace(/\*\*4/g, '⁴')
        .replace(/\*\*3/g, '³')
        .replace(/\*\*2/g, '²')
        .replace(/\*\*1/g, '¹');

    const polyLabel = lang === 'en' ? 'Polynomial' : 'Polinomio';

    const html = `<div class="solution-vector">
        <div class="solution-item">
            <span class="var-name">x</span>
            <span class="var-equals">=</span>
            <span class="var-value">${Number(xev).toFixed(10)}</span>
        </div>

        <div class="solution-item">
            <span class="var-name">P(x)</span>
            <span class="var-equals">=</span>
            <span class="var-value">${px_display}</span>
        </div>

        <div class="solution-item" style="margin-top:1rem;">
            <span class="var-name">${polyLabel}</span>
            <span class="var-equals">=</span>
            <span class="var-value">${polynomial}</span>
        </div>
    </div>`;
    container.innerHTML = html;

    if (window.I18n && typeof I18n.applyTranslations === 'function') {
        I18n.applyTranslations();
    }
}

/**
 * Renderiza la solución de búsqueda de raíces / integración.
 */
function renderRootSolution(result, containerId) {
    window.currentResult = result;
    const container = document.getElementById(containerId);
    if (!container) return;
    
    const root = result.root !== undefined ? result.root : result.solution[0];
    const iters = result.iterations || result.steps.length;

    let html = `<div class="solution-vector">
        <div class="solution-item">
            <span class="var-name">x*</span>
            <span class="var-equals">=</span>
            <span class="var-value">${Number(root).toFixed(10)}</span>
        </div>
        <div class="solution-item">
            <span class="var-name" data-i18n="iterations_label">Iterations</span>
            <span class="var-equals">=</span>
            <span class="var-value">${iters}</span>
        </div>`;

    if (result.intervals) {
        html += `<div class="solution-item">
            <span class="var-name" data-i18n="interval_label">Interval</span>
            <span class="var-equals">∈</span>
            <span class="var-value">[${result.intervals[0][0].toFixed(6)}, ${result.intervals[0][1].toFixed(6)}]</span>
        </div>`;
    }

    html += `</div>`;
    container.innerHTML = html;

    if (window.I18n && typeof I18n.applyTranslations === 'function') {
        I18n.applyTranslations();
    }
}

document.addEventListener('numcalc:langchange', function(e) {
    if (globalSteps && globalSteps.length > 0) {
        updateStepsView();
    }
    
    // Live-re-render active solution on language switch
    if (window.currentResult) {
        const mType = window.METHOD_TYPE || (typeof METHOD_TYPE !== 'undefined' ? METHOD_TYPE : '');
        if (mType === 'root') {
            renderRootSolution(window.currentResult, 'solution-container');
        } else if (mType === 'interpolation') {
            renderInterpSolution(window.currentResult, 'solution-container');
        } else {
            renderSolution(window.currentResult, 'solution-container');
        }
    }
});

