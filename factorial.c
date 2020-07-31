#include <stdio.h>
#include <cs50.h>


int factorial(int n)
{
    if (n == 1)
    {
        return 1;
    }
    else
    {
        return n * factorial(n - 1);
    }
}

int main(void)
{
    int input = get_int("Input :");
    printf("%i\n", factorial(input));
}

