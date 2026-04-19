def incremental_search(f, x0, h, N):
    print("Incremental Search\n")

    x_prev = x0
    f_prev = f(x_prev)

    print("| iter |    x_prev    |    x_curr    |   f(x_prev)   |   f(x_curr)   |")

    for i in range(1, N+1):
        x_curr = x_prev + h
        f_curr = f(x_curr)

        print(f"| {i:3} | {x_prev:12.6f} | {x_curr:12.6f} | {f_prev:12.6e} | {f_curr:12.6e} |")

        if f_prev * f_curr < 0:
            print(f"\nRoot found in interval [{x_prev}, {x_curr}]")
            return

        x_prev = x_curr
        f_prev = f_curr

    print("\nNo root interval found.")