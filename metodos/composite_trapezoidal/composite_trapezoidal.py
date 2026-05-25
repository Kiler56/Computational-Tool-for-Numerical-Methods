def composite_trapezoidal(f, a, b, n):
    """
    Composite Trapezoidal Method

    Approximates the definite integral of a function
    over the interval [a, b] using n subintervals.

    Parameters:
        f : function
            Function to integrate

        a : float
            Lower integration limit

        b : float
            Upper integration limit

        n : int
            Number of subintervals

    Returns:
        integral : float
            Approximate value of the integral
    """

    # Step size
    h = (b - a) / n

    # Generate nodes
    x = [a + i * h for i in range(n + 1)]

    # Evaluate function at each node
    y = [f(xi) for xi in x]

    # Apply composite trapezoidal formula
    integral = h * (
        sum(y) - 0.5 * (y[0] + y[-1])
    )

    print("\n===== COMPOSITE TRAPEZOIDAL METHOD =====\n")

    print("i\tXi\t\tf(Xi)")

    for i in range(n + 1):
        print(f"{i}\t{x[i]:.6f}\t{y[i]:.6f}")

    print("\nApproximate Integral:")
    print(integral)

    return integral