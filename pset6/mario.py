from cs50 import get_int
# defines space function


def space(n):
    for i in range(n):
        print(" ", end="")
# defines block funcion


def block(n):
    for i in range(n):
        print("#", end="")


n = - 1

# gets input from user
while n < 0 or n > 8:
    n = get_int("Height: ")
# prints blocks and spaces correctly
for i in range(n):
    space(n - i + 1)
    block(i + 1)
    print("\n", end="")
