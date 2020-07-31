#include "helpers.h"
#include "math.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //gets average value
            BYTE average = round((image[i][j].rgbtRed + image[i][j].rgbtBlue + image[i][j].rgbtGreen) / 3.0);
            //sets RBG value of each pixel to the average
            image[i][j].rgbtRed = average;
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //calculates sepia values for each pixel
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
            //caps sepia values at 255
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            //changes RGB values to new sepia values
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = temp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //creates 2 dimensional arrays to store new RBG values in
    int buffer_red[height][width];
    int buffer_blue[height][width];
    int buffer_green[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //creates counter and temporary variables
            int k = 0;
            float bufferred = 0;
            float bufferblue = 0;
            float buffergreen = 0;

            //includes neighbor value if neighbor pixel exists
            if (i > 0)
            {
                bufferred += image[i - 1][j].rgbtRed;
                bufferblue += image[i - 1][j].rgbtBlue;
                buffergreen += image[i - 1][j].rgbtGreen;
                k++;
            }
            //includes neighbor value if neighbor pixel exists
            if (i < height - 1)
            {
                bufferred += image[i + 1][j].rgbtRed;
                bufferblue += image[i + 1][j].rgbtBlue;
                buffergreen += image[i + 1][j].rgbtGreen;
                k++;
            }
            //includes neighbor value if neighbor pixel exists
            if (j > 0)
            {
                bufferred += image[i][j - 1].rgbtRed;
                bufferblue += image[i][j - 1].rgbtBlue;
                buffergreen += image[i][j - 1].rgbtGreen;
                k++;
            }
            //includes neighbor value if neighbor pixel exists
            if (j < width - 1)
            {
                bufferred += image[i][j + 1].rgbtRed;
                bufferblue += image[i][j + 1].rgbtBlue;
                buffergreen += image[i][j + 1].rgbtGreen;
                k++;
            }
            //includes neighbor value if neighbor pixel exists
            if (i > 0 && j > 0)
            {
                bufferred += image[i - 1][j - 1].rgbtRed;
                bufferblue += image[i - 1][j - 1].rgbtBlue;
                buffergreen += image[i - 1][j - 1].rgbtGreen;
                k++;
            }
            //includes neighbor value if neighbor pixel exists
            if (i > 0 && j < width - 1)
            {
                bufferred += image[i - 1][j + 1].rgbtRed;
                bufferblue += image[i - 1][j + 1].rgbtBlue;
                buffergreen += image[i - 1][j + 1].rgbtGreen;
                k++;
            }
            //includes neighbor value if neighbor pixel exists
            if (i < height - 1 && j > 0)
            {
                bufferred += image[i + 1][j - 1].rgbtRed;
                bufferblue += image[i + 1][j - 1].rgbtBlue;
                buffergreen += image[i + 1][j - 1].rgbtGreen;
                k++;
            }
            //includes neighbor value if neighbor pixel exists
            if (i < height - 1 && j < width - 1)
            {
                bufferred += image[i + 1][j + 1].rgbtRed;
                bufferblue += image[i + 1][j + 1].rgbtBlue;
                buffergreen += image[i + 1][j + 1].rgbtGreen;
                k++;
            }

            //includes own value
            bufferred += image[i][j].rgbtRed;
            bufferblue += image[i][j].rgbtBlue;
            buffergreen += image[i][j].rgbtGreen;
            k++;

            //puts blurred value into buffer arrays
            buffer_red[i][j] = round(bufferred / k);
            buffer_green[i][j] = round(buffergreen / k);
            buffer_blue[i][j] = round(bufferblue / k);

        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //changes image pixel values to buffer values
            image[i][j].rgbtRed = buffer_red[i][j];
            image[i][j].rgbtBlue = buffer_blue[i][j];
            image[i][j].rgbtGreen = buffer_green[i][j];
        }
    }
}

