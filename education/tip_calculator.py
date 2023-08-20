def tip_calculator(total=None):
    if not total:
        total = float(input("What is your total bill? "))
    tip = total * 0.2
    print(tip)

tip_calculator()
