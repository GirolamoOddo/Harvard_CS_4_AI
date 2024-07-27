#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

string apply_caesar(string _txt, int _key);

int main (int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    string str_check = argv[1];
    for (int i = 0, len = strlen(argv[1]); i < len; i++)
    {
        if (!(str_check[i] >= '0' && str_check[i] <= '9'))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    int key = atoi(argv[1]);
    string input_txt = get_string("plaintext:  ");
    string cipher_txt = apply_caesar(input_txt, key);
    printf("ciphertext: %s\n", cipher_txt);
    return 0;
}

string apply_caesar(string _txt, int _key)
{
   int _len = strlen(_txt);
   string _cip = _txt;

   for (int i = 0; i < _len; i++)
   {
     if (_txt[i]>= 'A' && _txt[i]<= 'Z')
     {
         _cip[i] = ((_txt[i] - 'A' + _key) % 26) + 'A';
     }
     else if (_txt[i]>= 'a'  && _txt[i]<= 'z')
     {
        _cip[i] = ((_txt[i] - 'a' + _key) % 26) + 'a';
     }
    }

    return _cip;
}
