**User Manual**

**Computational Tool for Numerical Methods**

**General Project Information**

Project name: Computational Tool for Numerical Methods

Official repository:  
[Computational Tool for Numerical Methods Repository](https://github.com/Kiler56/Computational-Tool-for-Numerical-Methods?utm_source=chatgpt.com)

The application was developed as an educational and computational tool focused on the learning, analysis, and practical application of numerical methods used in engineering, mathematics, and computational sciences.

The system allows students and engineers to:

- Execute different numerical methods.
- Analyze iterative results.
- Understand the conditions required to apply each method.
- Graphically visualize functions and numerical approximations.

The platform also integrates a graphing tool that facilitates the visual interpretation of the implemented algorithms.

**Table of Contents**

- Introduction
- Target Users
- System Requirements
- Installation and Application Access
- General Navigation
- Implemented Methods
- Integrated Graphing Tool
- Usage Recommendations
- Possible Errors
- Conclusions

**1\. Introduction**

Numerical methods are mathematical techniques used to solve problems that cannot easily be solved through exact analytical methods.

This tool brings together different classical algorithms used in:

- Root finding.
- Solving systems of equations.
- Interpolation.
- Numerical integration.
- Ordinary differential equations.

The main purpose of the application is to strengthen practical learning through simulations, iterations, and graphical visualization of numerical methods.

**2\. Target Users**

This tool is mainly intended for:

- Systems engineering students.
- Mathematical engineering students.
- Applied science students.
- Professors and instructors.
- Users interested in numerical methods.

**3\. System Requirements**

**Minimum Requirements**

- Windows, Linux, or macOS operating system.
- Python installed.
- Modern web browser or compatible graphical environment.
- Local connection for project execution.

**Recommended Requirements**

- 8 GB RAM or higher.
- Multi-core processor.
- Full HD resolution.

**4\. Installation and Application Access**

The application was successfully deployed and can be used both online and locally.

**Web Access**

Users can directly access the platform through the following link:

<http://54.88.246.211:5000/>

From this environment, users can execute all implemented numerical methods, perform iterative calculations, and visualize results using the integrated graphing tool.

**Local Execution**

If the user wants to run the application locally, the following steps must be followed.

**Step 1: Clone the repository**

git clone <https://github.com/Kiler56/Computational-Tool-for-Numerical-Methods.git>

**Step 2: Enter the project directory**

cd Computational-Tool-for-Numerical-Methods

**Step 3: Install dependencies**

pip install -r requirements.txt

**Step 4: Run the application**

python main.py

Note: Depending on the project structure, the main file may vary.

**Access Recommendations**

- It is recommended to use updated web browsers.
- Verify internet connection for web access.
- For local execution, make sure Python and all dependencies are properly installed.

**5\. General Application Navigation**

The platform is organized into modules of numerical methods.

Each section includes:

- Basic explanation of the method.
- Required inputs.
- Validations.
- Iterative tables.
- Numerical results.
- Graphical visualization.

The interface allows navigation between different categories of methods through the main menu.

**6\. Implemented Methods**

**6.1 Root-Finding Methods**

These methods allow finding solutions of nonlinear equations.

**Available Methods**

- Incremental Search
- Bisection
- False Position
- Fixed Point
- Newton
- Secant
- Multiple Roots

**Incremental Search**

Description:

Method used to detect intervals where a root may exist through sign changes.

Requirements:

- The function must be continuous.
- An exploration interval must exist.

Results:

- Candidate intervals
- Iterative table
- Graphical representation

**Bisection Method**

Description:

Iterative method that continuously divides an interval to approximate a root.

Requirements:

- The function must be continuous.
- A sign change must exist within the interval.

Results:

- Root approximation
- Calculated error
- Iterative table
- Function graph

**False Position Method**

Description:

Method similar to bisection but using linear interpolation to approximate the root.

Requirements:

- Sign change in the interval.
- Continuous function.

Results:

- Root approximation
- Relative error
- Iteration table

**Fixed Point Method**

Description:

Iterative method based on the transformation x = g(x).

Requirements:

- The transformed function must converge.
- The derivative of g(x) must satisfy convergence conditions.

Results:

- Root approximation
- Performed iterations
- Obtained error

**Newton Method**

Description:

Derivative-based method used to rapidly approximate roots.

Requirements:

- The function must be differentiable.
- The derivative must not be zero near the root.

Results:

- Root approximation
- Iterations
- Error
- Graphical visualization

**Secant Method**

Description:

Iterative method that approximates the derivative using two initial values.

Results:

- Numerical approximation
- Iterative error
- Results table

**Multiple Roots Method**

Description:

Method designed for functions with repeated roots.

Results:

- Multiple root approximation
- Iterative convergence

**6.2 Systems of Linear Equations**

These methods allow solving matrix systems.

**Available Methods**

- Gaussian Elimination
- Partial Pivoting
- Total Pivoting
- Simple LU
- LU Pivoting
- Crout
- Doolittle
- Cholesky
- Jacobi
- Gauss-Seidel
- SOR

**Gaussian Elimination**

Description:

Transforms the system into an upper triangular matrix.

Results:

- System solution
- Step-by-step procedure

**Partial Pivoting**

Description:

Swaps rows to improve numerical stability.

Results:

- Transformed matrix
- Stable solution

**Total Pivoting**

Description:

Swaps rows and columns to avoid numerical errors.

Results:

- Improved computational stability
- System solution

**LU Factorization**

Included methods:

- Simple LU
- LU Pivoting
- Crout
- Doolittle
- Cholesky

Description:

Decomposes a matrix into matrix products to solve linear systems.

Results:

- Factorized matrices
- System solution

**Iterative Methods**

Included methods:

- Jacobi
- Gauss-Seidel
- SOR

Description:

Approximation methods used to solve linear systems.

Results:

- Iterative approximations
- Error per iteration
- Convergence

**6.3 Interpolation**

These methods allow approximating functions from sets of points.

**Available Methods**

- Vandermonde
- Newton (Divided Differences)
- Lagrange

**Vandermonde Method**

Description:

Builds a matrix system using the given points to obtain the interpolating polynomial.

Results:

- Vandermonde matrix
- Interpolating polynomial
- Graphical evaluation

**Newton Divided Differences Method**

Description:

Constructs the interpolating polynomial using successive divided differences.

Results:

- Divided differences table
- Interpolating polynomial
- Graphical approximation

**Lagrange Method**

Description:

Generates an interpolating polynomial using basis polynomials.

Results:

- Interpolating polynomial
- Numerical evaluation
- Graphical representation

**6.4 Numerical Integration**

Allows approximation of definite integrals.

**Available Methods**

- Composite Trapezoidal Method
- Composite Simpson 1/3 Method
- Simple Simpson 3/8 Method

**Composite Trapezoidal Method**

Description:

Approximates the area under the curve using successive trapezoids.

Results:

- Integral approximation
- Approximate error
- Area graph

**Composite Simpson 1/3 Method**

Results:

- Area approximation
- Calculation table
- Graphical representation

**Simple Simpson 3/8 Method**

Description:

Uses cubic interpolation to approximate integrals.

Results:

- Numerical approximation
- Graphically visualized area

**6.5 Differential Equations**

Methods for approximating solutions of ordinary differential equations.

**Available Methods**

- Euler
- Heun

**Euler Method**

Description:

Basic method for approximating solutions of initial value problems.

Results:

- Approximation table
- Graphical solution

**Heun Method**

Description:

Improves Euler's approximation using an average slope approach.

Results:

- Refined approximation
- Graphical comparison
- Reduced error

**7\. Integrated Graphing Tool**

The application includes a graphical tool that allows visualization of:

- Mathematical functions.
- Iterative behavior.
- Numerical approximations.
- Method convergence.
- Interpolations.
- Approximate solutions.

Main functionalities:

- Function graphing.
- Root visualization.
- Comparison between methods.
- Representation of interpolated points.
- Visualization of iterative convergence.

The graphing tool facilitates visual understanding and mathematical analysis of each algorithm.

**8\. Usage Recommendations**

- Verify the correct syntax of mathematical functions.
- Use valid intervals.
- Review convergence conditions.
- Define appropriate tolerances.
- Validate matrix conditions before running iterative methods.

**9\. Possible Errors**

| **Error**                | **Possible Cause**                |
| ------------------------ | --------------------------------- |
| Division by zero         | Null derivative or invalid pivot  |
| Method does not converge | Poor initial approximation        |
| Invalid interval         | No sign change exists             |
| Singular matrix          | The system has no unique solution |
| Interpolation error      | Insufficient or repeated data     |

**10\. Conclusions**

The tool provides an educational and interactive environment for understanding and applying classical numerical methods through computational simulation and graphical analysis.

The integration of mathematical algorithms, iterative tables, and graphical visualization strengthens practical learning in engineering, mathematics, and computational sciences.

The system facilitates both theoretical understanding and practical experimentation with the implemented methods.
