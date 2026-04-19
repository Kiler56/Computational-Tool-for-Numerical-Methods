def trisection(f, a, b, tol=1e-7, N=100):
    print("\nTrisection\n")

    if f(a) * f(b) > 0:
        print("Warning: no guaranteed root in interval.")

    E = None

    print("| iter |      a       |      x1      |      x2      |      b       |     E     |")

    for i in range(1, N+1):
        x1 = a + (b - a)/3
        x2 = b - (b - a)/3

        if E is None:
            print(f"| {i:3} | {a:12.6f} | {x1:12.6f} | {x2:12.6f} | {b:12.6f} |           |")
        else:
            print(f"| {i:3} | {a:12.6f} | {x1:12.6f} | {x2:12.6f} | {b:12.6f} | {E:10.6e} |")

        if f(a)*f(x1) < 0:
            b = x1
        elif f(x1)*f(x2) < 0:
            a = x1
            b = x2
        else:
            a = x2

        E = abs(b - a)

        if E < tol:
            break

    xm = (a + b)/2
    print(f"\nApproximate root: {xm}")