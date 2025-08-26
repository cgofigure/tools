def quadratic():
    a = float(input("Enter a: "))
    b = float(input("Enter b: "))
    c = float(input("Enter c: "))

    root_a = (-b + (b * b - 4 * a * c) ** 0.5) / (2 * a)
    root_b = (-b - (b * b - 4 * a * c) ** 0.5) / (2 * a)

    print(root_a)
    print(root_b)

quadratic()
