#include <cs50.h>
#include <stdio.h>

void build_pyramids(int _brks);

int main(void)
{
    int bricks;
    do
    {
        bricks = get_int("Heigth:");
    }
    while (bricks <= 0);

    build_pyramids(bricks + 1);
}

void build_pyramids(int _brks)
{
    for (int i = 1; i < _brks; i++)
    {
        for (int j = 1; j < _brks - i; j++)
        {
            printf(" ");
        }
        for (int k = 0; k < i; k++)
        {
            printf("#");
        }
        printf("  ");

        for (int w = 0; w < i; w++)
        {
            printf("#");
        }
        printf("\n");
    }
}
