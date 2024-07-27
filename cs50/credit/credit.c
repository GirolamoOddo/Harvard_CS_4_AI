#include <stdio.h>
#include <cs50.h>

bool is_valid(unsigned long long card_number);
string card_type(unsigned long long card_number);


int main(void)
{
    unsigned long long card_number;

    do
    {
        card_number = get_long("Number: ");
    }
    while (card_number <= 0);

    if (is_valid(card_number))
    {
        printf("%s\n", card_type(card_number));
    }
    else
    {
        printf("INVALID\n");
    }

    return 0;
}


bool is_valid(unsigned long long card_number)
{
    int sum = 0;
    bool multiply = false;

    while (card_number > 0)
    {
        int digit = card_number % 10;
        card_number /= 10;

        if (multiply)
        {
            digit *= 2;
            digit = (digit % 10) + (digit / 10);
        }

        sum += digit;
        multiply = !multiply;
    }

    return (sum % 10 == 0);
}

string card_type(unsigned long long card_number)
{
    int length = 0;
    unsigned long long temp = card_number;

    while (temp > 0)
    {
        temp /= 10;
        length++;
    }

    if ((length == 15) && ((card_number / 10000000000000 == 34) || (card_number / 10000000000000 == 37)))
    {
        return "AMEX";
    }
    else if ((length == 16) && ((card_number / 100000000000000 == 51) || (card_number / 100000000000000 == 52) || (card_number / 100000000000000 == 53) || (card_number / 100000000000000 == 54) || (card_number / 100000000000000 == 55)))
    {
        return "MASTERCARD";
    }
    else if (((length == 13) || (length == 16)) && ((card_number / 1000000000000000 == 4) || (card_number / 1000000000000 == 4))) // Corrected condition for VISA
    {
        return "VISA";
    }
    else
    {
        return "INVALID";
    }
}

