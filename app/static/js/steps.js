/**
 * steps.js — Render intermediate steps.
 */

function renderSteps(steps, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    steps.forEach((step, index) => {
        const stepEl = document.createElement('div');
        stepEl.className = 'step-card';
        stepEl.style.animationDelay = `${index * 0.05}s`;

        let badges = '';
        if (step.swap_rows) {
            badges += `<span class="badge badge-swap">↕ Rows ${step.swap_rows[0]+1} ↔ ${step.swap_rows[1]+1}</span>`;
        }
        if (step.swap_cols) {
            badges += `<span class="badge badge-swap-col">↔ Cols ${step.swap_cols[0]+1} ↔ ${step.swap_cols[1]+1}</span>`;
        }

        let phaseLabel = '';
        if (step.phase === 'elimination') phaseLabel = 'Elimination';
        else if (step.phase === 'forward_sweep') phaseLabel = 'Forward sweep';
        else if (step.phase === 'back_substitution') phaseLabel = 'Back substitution';
        else if (step.phase === 'extract') phaseLabel = 'Extract';
        else if (step.phase === 'reorder') phaseLabel = 'Reorder';
        else if (step.phase === 'lagrange_setup') phaseLabel = 'Lagrange setup';
        else if (step.phase === 'lagrange_basis') phaseLabel = 'Basis L_j';
        else if (step.phase === 'lagrange_sum') phaseLabel = 'Sum terms';

        stepEl.innerHTML = `
            <div class="step-header">
                <span class="step-number">${step.step}</span>
                <span class="step-phase">${phaseLabel}</span>
                ${badges}
            </div>
            <p class="step-desc">${step.description}</p>
        `;

        // Matrix snapshot when present
        if (step.matrix_state) {
            stepEl.appendChild(buildMatrixTable(step.matrix_state));
        }

        // Thomas: show diagonals and RHS
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

/** Render solution vector with 6 decimals. */
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
