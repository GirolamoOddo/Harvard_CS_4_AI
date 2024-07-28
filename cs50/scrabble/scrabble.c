#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int compute_points(string _input_string);
void return_winner(int p_1, int p_2);
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int main(void)
{
    string string_1 = get_string("Player 1: ");
    string string_2 = get_string("Player 2: ");

    int p1_points = compute_points(string_1);
    int p2_points = compute_points(string_2);

    return_winner(p1_points, p2_points);
}

int compute_points(string _input_string)
{
    int _points = 0;
    int _length = strlen(_input_string);

    for (int i = 0; i < _length; i++)
    {
     _input_string[i] = toupper(_input_string[i]);

     if (_input_string[i]>= 65 && _input_string[i]<= 90)
     {
        _points += POINTS[_input_string[i] - 'A'];
     }
     else
     {
        _points += 0;
     }
    }

    return _points;
}

void return_winner(int p_1, int p_2)
{
    if (p_1 > p_2)
    {
       printf("Player 1 wins!\n");
    }
    else if (p_1 < p_2)
    {
       printf("Player 2 wins!\n");
    }
    else
    {
       printf("Tie!\n");
    }
}
