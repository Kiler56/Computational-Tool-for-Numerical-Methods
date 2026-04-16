/**
 * steps.js — Renderiza los pasos intermedios y la solución final.
 */

/**
 * Renderiza la lista de pasos dentro del contenedor indicado.
 */
function renderSteps(steps, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    steps.forEach((step, index) => {
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

        container.appendChild(stepEl);
    });
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
 * Renderiza el vector solución con 6 decimales.
 */
function renderSolution(solution, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

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
