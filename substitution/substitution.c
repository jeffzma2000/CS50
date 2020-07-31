#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    //store user input for the key in a variable
    string key = argv[1];
    //deals with case that user doesn't put in a key
    if (argc < 2)
    {
        printf("Error: put in a key.\n");
        return 1;
    }
    //deals with case when there are more than two keys
    if (argc > 2)
    {
        printf("Error: more than one argument.\n");
        return 1;
    }
    //deals with case when key is not 26 letters
    if (strlen(key) != 26)
    {
        printf("Error: key must be 26 letters.\n");
        return 1;
    }
    //deals with case when key has repeated letters
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            if (key[j] == key[i])
            {
                printf("Error: key cannot repeat letters.\n");
                return 1;
            }
        }
        //deals with case when a character is not alphabetical
        if (isalpha(key[i]) == 0)
        {
            printf("Error: key must be alphabetical.\n");
            return 1;
        }
    }

    //prompts user for their plain text
    string plaintext = get_string("plaintext: ");
    //creates normal alphabets to convert with user's key
    string normal = "abcdefghijklmnopqrstuvwxyz";
    string upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    //print ciphertext:
    printf("ciphertext: ");
    //iterates through plaintext
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        //iterates through alphabet
        for (int j = 0, m = strlen(normal); j < m; j++)
        {
            //convert lowercase plaintext to lowercase key value
            if (plaintext[i] == normal[j])
            {
                printf("%c", tolower(key[j]));
            }
            //convert uppercase plaintext to uppercase key value
            if (plaintext[i] == upper[j])
            {
                printf("%c", toupper(key[j]));
            }
        }
        //maintains plaintext values that are not alphabetical
        if (isalpha(plaintext[i]) == 0)
        {
            printf("%c", plaintext[i]);
        }
    }
    //creates a new line
    printf("\n");
    //exits from main
    return 0;
}