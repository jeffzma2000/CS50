#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    //check to see there is a single file
    if (argc > 2)
    {
        printf("Enter a single file.");
        return 1;
    }
    //opens file
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Enter a valid file.");
        return 1;
    }
    //creates a buffer array to store into
    unsigned char buffer[512];
    //creates an array to write pics into
    char pics[50];
    //creates a counter variable
    int n = 0;
    //reads 512 blocks from file into buffer
    while (fread(buffer, 512, 1, file) == 1)
    {
        //checks if it is the beginning of a jpeg and writes it into a new jpg file
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            sprintf(pics, "%03i.jpg", n);
            FILE *jpegs = fopen(pics, "w");
            fwrite(buffer, 512, 1, jpegs);
            //checks to see if the file is more than 512 bytes
            while (fread(buffer, 512, 1, file) == 1)
            {
                if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
                {
                    fclose(jpegs);
                    break;
                }
                else
                {
                    fwrite(buffer, 512, 1, jpegs);
                }
            }
            //corrects for skipping files
            fseek(file, -512, SEEK_CUR);
            //updates counter
            n++;
        }
    }
}
