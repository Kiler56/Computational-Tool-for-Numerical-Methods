/**
 * plotter.js — Universal Frontend Plotting Module using Plotly.js
 */

const MathPlotter = {
    /**
     * Parse and evaluate a math expression string using Javascript Math
     * or a safe eval wrapper. For basic functions:
     */
    evaluateExpr: function(expr, x) {
        // Simple regex replace to make expression JS compatible
        // Note: In a real app we'd use math.js, but since we are replacing backend sympify
        // we map basic python-like math to JS Math object
        let jsExpr = expr.replace(/\*\*/g, '**');
        jsExpr = jsExpr.replace(/\bsin\b/g, 'Math.sin');
        jsExpr = jsExpr.replace(/\bcos\b/g, 'Math.cos');
        jsExpr = jsExpr.replace(/\btan\b/g, 'Math.tan');
        jsExpr = jsExpr.replace(/\bexp\b/g, 'Math.exp');
        jsExpr = jsExpr.replace(/\blog\b/g, 'Math.log');
        jsExpr = jsExpr.replace(/\bsqrt\b/g, 'Math.sqrt');
        jsExpr = jsExpr.replace(/\babs\b/g, 'Math.abs');
        jsExpr = jsExpr.replace(/\bpi\b/g, 'Math.PI');
        jsExpr = jsExpr.replace(/\be\b/g, 'Math.E');

        try {
            // Function constructor is safer than eval, isolated scope
            const func = new Function('x', 'return ' + jsExpr);
            return func(x);
        } catch (e) {
            console.error("Failed to evaluate expression:", jsExpr, e);
            return null;
        }
    },

    /**
     * Plot a function f(x)
     * @param {string} containerId - DOM element ID
     * @param {string} expr - Math expression e.g., 'x**2 - 2'
     * @param {number} xMin 
     * @param {number} xMax 
     * @param {number} root - Optional root to mark
     */
    plotFunction: function(containerId, expr, xMin = -10, xMax = 10, root = null) {
        const xValues = [];
        const yValues = [];
        const step = (xMax - xMin) / 200;

        for (let x = xMin; x <= xMax; x += step) {
            const y = this.evaluateExpr(expr, x);
            if (y !== null && !isNaN(y) && isFinite(y)) {
                xValues.push(x);
                yValues.push(y);
            }
        }

        const data = [{
            x: xValues,
            y: yValues,
            type: 'scatter',
            mode: 'lines',
            name: 'f(x)',
            line: { color: '#0066cc', width: 2 }
        }];

        if (root !== null) {
            data.push({
                x: [root],
                y: [0],
                type: 'scatter',
                mode: 'markers',
                name: 'Root',
                marker: { color: 'red', size: 10 }
            });
        }

        const layout = {
            title: 'Function Plot',
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            xaxis: { title: 'x', zeroline: true },
            yaxis: { title: 'f(x)', zeroline: true },
            margin: { l: 40, r: 40, b: 40, t: 40 }
        };

        Plotly.newPlot(containerId, data, layout, {responsive: true});
    },

    /**
     * Plot interpolation points and polynomial
     */
    plotInterpolation: function(containerId, pointsX, pointsY, polyExpr, evalX = null, evalY = null) {
        // Original Points
        const data = [{
            x: pointsX,
            y: pointsY,
            type: 'scatter',
            mode: 'markers',
            name: 'Nodes',
            marker: { color: 'red', size: 8 }
        }];

        // Generate line for polynomial if available
        if (polyExpr) {
            const minX = Math.min(...pointsX);
            const maxX = Math.max(...pointsX);
            const margin = (maxX - minX) * 0.1 || 1;
            
            const xLine = [];
            const yLine = [];
            const step = (maxX - minX + 2*margin) / 200;
            
            for (let x = minX - margin; x <= maxX + margin; x += step) {
                const y = this.evaluateExpr(polyExpr, x);
                if (y !== null && !isNaN(y) && isFinite(y)) {
                    xLine.push(x);
                    yLine.push(y);
                }
            }
            
            data.unshift({
                x: xLine,
                y: yLine,
                type: 'scatter',
                mode: 'lines',
                name: 'P(x)',
                line: { color: '#0066cc', width: 2, shape: 'spline' }
            });
        }

        // Evaluation Point
        if (evalX !== null && evalY !== null) {
            data.push({
                x: [evalX],
                y: [evalY],
                type: 'scatter',
                mode: 'markers',
                name: 'P(x_eval)',
                marker: { color: '#ff9900', size: 10, symbol: 'star' }
            });
        }

        const layout = {
            title: 'Interpolation Plot',
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            xaxis: { title: 'x' },
            yaxis: { title: 'P(x)' },
            margin: { l: 40, r: 40, b: 40, t: 40 }
        };

        Plotly.newPlot(containerId, data, layout, {responsive: true});
    }
};
