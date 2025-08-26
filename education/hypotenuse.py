def hypotenuse(a=None, b=None):
    if not a:
        a = float(input("What is the length of side A? "))

    if not b:
        b = float(input("What is the length of side B? "))

    c = (a * a + b * b) ** 0.5
    print(c)
