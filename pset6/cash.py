from cs50 import get_float

n = -1

# makes sure the input is positive


while n < 0:
    n = get_float("Change owed: ")

# changes input to change


change = n * 100

# sets number of coins to 0


coins = 0

# checks quarters


while change >= 25:
    change = change - 25
    coins += 1
# checks dimes


while change >= 10:
    change = change - 10
    coins += 1
# checks nickels


while change >= 5:
    change = change - 5
    coins += 1
# checks pennies


while change >= 1:
    chang = change - 1
    coins += 1
# prints number of coins


print(coins)