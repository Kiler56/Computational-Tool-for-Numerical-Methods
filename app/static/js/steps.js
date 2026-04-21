/**
 * steps.js — Renderiza los pasos intermedios y la solución final.
 */

let globalSteps = [];
let currentStepIndex = 0;
let currentViewMode = 'all'; // 'all' or 'step'

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
    if (display) display.textContent = `Paso ${currentStepIndex + 1} de ${globalSteps.length}`;
}

function createStepElement(step, index) {
    const stepEl = document.createElement('div');
    stepEl.className = 'step-card';
    stepEl.style.animationDelay = `${index * 0.05}s`;

    // Encabezado del paso
    let badges = '';
    if (step.swap_rows) {
        badges += `<span class="badge badge-swap">↕ Filas ${step.swap_rows[0]+1} ↔ ${step.swap_rows[1]+1}</span>`;
    }
    if (step.swap_cols) {
        badges += `<span class="badge badge-swap-col">↔ Cols ${step.swap_cols[0]+1} ↔ ${step.swap_cols[1]+1}</span>`;
    }

    let phaseLabel = '';
    if (step.phase === 'elimination') phaseLabel = 'Eliminación';
    else if (step.phase === 'forward_sweep') phaseLabel = 'Forward Sweep';
    else if (step.phase === 'back_substitution') phaseLabel = 'Sustitución';
    else if (step.phase === 'extract') phaseLabel = 'Extracción';
    else if (step.phase === 'reorder') phaseLabel = 'Reorden';
    else if (step.phase === 'analysis') phaseLabel = 'Análisis';

    stepEl.innerHTML = `
        <div class="step-header">
            <span class="step-number">${step.step}</span>
            <span class="step-phase">${phaseLabel}</span>
            ${badges}
        </div>
        <p class="step-desc">${step.description}</p>
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

/**
 * Construye una tabla HTML a partir de una matriz 2D.
 */
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

/**
 * Renderiza el vector solución y propiedades de la matriz.
 */
function renderSolution(result, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    // Propiedades de la matriz
    if (result.properties) {
        const propsDiv = document.createElement('div');
        propsDiv.className = 'matrix-properties callout callout-info';
        propsDiv.style.marginBottom = '1.5rem';
        let propsHtml = '<h3 style="margin-top:0;">Propiedades de la Matriz</h3><ul style="margin-bottom:0;">';
        for (const [key, value] of Object.entries(result.properties)) {
            propsHtml += `<li><strong>${key}:</strong> ${value}</li>`;
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
        lContainer.innerHTML = '<h4 style="margin-bottom:0.5rem; text-align:center;">Matriz L:</h4>';
        lContainer.appendChild(buildMatrixTable(result.L));
        luDiv.appendChild(lContainer);
        
        const uContainer = document.createElement('div');
        uContainer.innerHTML = '<h4 style="margin-bottom:0.5rem; text-align:center;">Matriz U:</h4>';
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
}
