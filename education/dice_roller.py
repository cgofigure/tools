import random

def roll(sides=None, times=1):
    roll_value = []
    
    if not sides:
        sides = 20

    for i in range(0, times):
        num = random.randint(1, sides)
        print(num)
        roll_value.append(num)

    total_roll = sum(roll_value)

    return total_roll

print(roll(sides=12, times=2))