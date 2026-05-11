def newton_interpolation(X, Y):
    n = len(X)

    # Initialize divided differences table
    D = [[0 for _ in range(n)] for _ in range(n)]

    # First column = Y values
    for i in range(n):
        D[i][0] = Y[i]

    # Compute divided differences
    for j in range(1, n):
        for i in range(j, n):
            D[i][j] = (
                (D[i][j - 1] - D[i - 1][j - 1]) /
                (X[i] - X[i - j])
            )

    # Extract coefficients from diagonal
    coef = [D[i][i] for i in range(n)]

    # Print divided differences table
    print("\nDivided Differences Table:\n")

    for row in D:
        print(["{:.6f}".format(value) for value in row])

    print("\nNewton Polynomial Coefficients:")
    print(coef)

    return coef