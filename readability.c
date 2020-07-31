#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>

//setting variable counters
int letters = 0;
int words = 1;
int sentences = 0;
int main(void)
{
    //prompts user for text input
    string s = get_string("Text: \n");
    //stores length of the string input
    int length = strlen(s);

    //takes care of the case where first character is a space
    if (s[0] == 32)
    {
        words = words - 1;
    }
    //takes care of the case where the last character is a space
    if (s[length - 1] == 32)
    {
        words = words - 1;
    }

    //iterates through the characters in the string
    for (int i = 0; i < length; i++)
    {
        //counts letters
        if ((s[i] >= 65 && s[i] <= 90) || (s[i] >= 97 && s[i] <= 122))
        {
            letters++;
        }
        //counts words
        if (s[i] == 32 && s[i - 1] != 32)
        {
            words++;
        }
        //counts sentences
        if ((s[i] == 46 || s[i] == 33 || s[i] == 63))
        {
            sentences++;
        }

    }



    //calculations for index
    double L = (double) letters / (double) words * 100;
    double S = (double) sentences / (double) words * 100;
    double index =  0.0588 * (double) L - 0.296 * (double) S - 15.8;
    int grade = round(index);

    //output
    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }

}
