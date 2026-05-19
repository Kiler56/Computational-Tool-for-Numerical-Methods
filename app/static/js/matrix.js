/**
 * matrix.js — Genera y lee dinámicamente los grids de inputs para la matriz A y vector b.
 */

/**
 * Genera una grilla de inputs nxn dentro del contenedor indicado.
 */
function buildMatrixGrid(n, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    container.style.gridTemplateColumns = `repeat(${n}, 1fr)`;

    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            const input = document.createElement('input');
            input.type = 'number';
            input.step = 'any';
            input.className = 'matrix-input';
            input.id = `a-${i}-${j}`;
            input.placeholder = `a${i+1}${j+1}`;
            input.setAttribute('aria-label', `Elemento a${i+1}${j+1}`);
            container.appendChild(input);
        }
    }
}

/**
 * Genera una columna de n inputs para el vector b.
 */
function buildVectorGrid(n, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';

    for (let i = 0; i < n; i++) {
        const input = document.createElement('input');
        input.type = 'number';
        input.step = 'any';
        input.className = 'matrix-input vector-input';
        input.id = `b-${i}`;
        input.placeholder = `b${i+1}`;
        input.setAttribute('aria-label', `Elemento b${i+1}`);
        container.appendChild(input);
    }
}

/**
 * Lee los valores de la grilla y los devuelve como number[][].
 * Retorna null si algún campo está vacío.
 */
function readMatrix(containerId, n) {
    const matrix = [];
    for (let i = 0; i < n; i++) {
        const row = [];
        for (let j = 0; j < n; j++) {
            const el = document.getElementById(`a-${i}-${j}`);
            if (!el || el.value === '') return null;
            row.push(parseFloat(el.value));
        }
        matrix.push(row);
    }
    return matrix;
}

/**
 * Lee los valores del vector b y los devuelve como number[].
 * Retorna null si algún campo está vacío.
 */
function readVector(containerId, n) {
    const vec = [];
    for (let i = 0; i < n; i++) {
        const el = document.getElementById(`b-${i}`);
        if (!el || el.value === '') return null;
        vec.push(parseFloat(el.value));
    }
    return vec;
}

/**
 * Genera una grilla de inputs Nx2 para puntos (X, Y).
 */
function buildPointsGrid(n, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    // Create header row
    const xLabel = document.createElement('div');
    xLabel.textContent = 'X';
    xLabel.style.fontWeight = 'bold';
    xLabel.style.textAlign = 'center';
    
    const yLabel = document.createElement('div');
    yLabel.textContent = 'Y';
    yLabel.style.fontWeight = 'bold';
    yLabel.style.textAlign = 'center';
    
    container.appendChild(xLabel);
    container.appendChild(yLabel);

    for (let i = 0; i < n; i++) {
        const xInput = document.createElement('input');
        xInput.type = 'number';
        xInput.step = 'any';
        xInput.className = 'matrix-input';
        xInput.id = `pt-x-${i}`;
        xInput.placeholder = `x${i+1}`;
        xInput.setAttribute('aria-label', `Punto X${i+1}`);
        container.appendChild(xInput);
        
        const yInput = document.createElement('input');
        yInput.type = 'number';
        yInput.step = 'any';
        yInput.className = 'matrix-input';
        yInput.id = `pt-y-${i}`;
        yInput.placeholder = `y${i+1}`;
        yInput.setAttribute('aria-label', `Punto Y${i+1}`);
        container.appendChild(yInput);
    }
}

/**
 * Lee los valores de los puntos y devuelve {x: number[], y: number[]}.
 * Retorna null si algún campo está vacío.
 */
function readPoints(n) {
    const xPoints = [];
    const yPoints = [];
    for (let i = 0; i < n; i++) {
        const xEl = document.getElementById(`pt-x-${i}`);
        const yEl = document.getElementById(`pt-y-${i}`);
        if (!xEl || xEl.value === '' || !yEl || yEl.value === '') return null;
        xPoints.push(parseFloat(xEl.value));
        yPoints.push(parseFloat(yEl.value));
    }
    return { x: xPoints, y: yPoints };
}
