#include "helpers.h"

int _round(float number)
{
    if (number >= 0)
    {
        return (int)(number + 0.5);
    }
    else
    {
        return (int)(number - 0.5);
    }
}

int _clip(int value, int min, int max)
{
    if (value < min)
    {
        return min;
    }
    else if (value > max)
    {
        return max;
    }
    else
    {
        return value;
    }
}

void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int _avg = _round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue  = _avg;
            image[i][j].rgbtGreen = _avg;
            image[i][j].rgbtRed   = _avg;
        }
    }
    return;
}

void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int _org_blue, _org_green, _org_red;
    int _new_blue, _new_green, _new_red;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            _org_blue  = image[i][j].rgbtBlue;
            _org_green = image[i][j].rgbtGreen;
            _org_red   = image[i][j].rgbtRed;

            _new_blue  = _round(.272 * _org_red + .534 * _org_green + .131 * _org_blue);
            _new_green = _round(.349 * _org_red + .686 * _org_green + .168 * _org_blue);
            _new_red   = _round(.393 * _org_red + .769 * _org_green + .189 * _org_blue);

            image[i][j].rgbtBlue  = _clip(_new_blue, 0, 255);
            image[i][j].rgbtGreen = _clip(_new_green, 0, 255);
            image[i][j].rgbtRed   = _clip(_new_red, 0, 255);
        }
    }
    return;
}

void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE _temp;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            _temp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = _temp;
        }
    }
    return;
}

void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int _sumRed = 0, _sumGreen = 0, _sumBlue = 0;
            int _count  = 0;

            for (int di = -1; di <= 1; di++)
            {
                for (int dj = -1; dj <= 1; dj++)
                {
                    int ni = i + di;
                    int nj = j + dj;

                    if (ni >= 0 && ni < height && nj >= 0 && nj < width)
                    {
                        _sumRed   += copy[ni][nj].rgbtRed;
                        _sumGreen += copy[ni][nj].rgbtGreen;
                        _sumBlue  += copy[ni][nj].rgbtBlue;
                        _count++;
                    }
                }
            }

            image[i][j].rgbtRed   = _round((float)_sumRed / _count);
            image[i][j].rgbtGreen = _round((float)_sumGreen / _count);
            image[i][j].rgbtBlue  = _round((float)_sumBlue / _count);
        }
    }
    return;
}
