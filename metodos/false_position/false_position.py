def false_position(f, a, b, tol=1e-7, N=100):
    print("\nFalse Position\n")

    if f(a) * f(b) > 0:
        print("Invalid interval: no sign change.")
        return

    fa = f(a)
    fb = f(b)

    xm = (fb*a - fa*b) / (fb - fa)
    E = None

    print("| iter |      a       |      xm      |      b       |    f(xm)    |     E     |")

    for i in range(1, N+1):
        fxm = f(xm)

        if E is None:
            print(f"| {i:3} | {a:12.6f} | {xm:12.6f} | {b:12.6f} | {fxm:12.6e} |           |")
        else:
            print(f"| {i:3} | {a:12.6f} | {xm:12.6f} | {b:12.6f} | {fxm:12.6e} | {E:10.6e} |")

        if fa * fxm < 0:
            b = xm
            fb = f(b)
        else:
            a = xm
            fa = f(a)

        x_old = xm
        xm = (fb*a - fa*b) / (fb - fa)
        E = abs(xm - x_old)

        if E < tol:
            break

    print(f"\nApproximate root: {xm}")