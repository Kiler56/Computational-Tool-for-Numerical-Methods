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
