#include <cs50.h>
#include <math.h>

#include <ctype.h>
#include <stdio.h>

#include <stdlib.h>
#include <string.h>

int get_letters(  char input_text[], int len);
int get_words(    char input_text[], int len);
int get_sentences(char input_text[], int len);
int ColemanLiau_Idx(int letters, int words, int sentences);

int main (void)
{
    string input_text = get_string("Text: ");
    int length        = strlen(input_text);

    int letters   = get_letters(  input_text, length);
    int words     = get_words(    input_text, length);
    int sentences = get_sentences(input_text, length);

    int index     = ColemanLiau_Idx(letters, words, sentences);

    if (index < 1)
        printf("Before Grade 1\n");

    else if(index > 16)
        printf("Grade 16+\n");

    else
        printf("Grade %i\n", index);
}

int get_letters(char input_text[], int len)
{
    int letters = 0;
    for (int i = 0; i < len; i++)
    {
        if ((input_text[i] >= 'a' && input_text[i] <= 'z') || (input_text[i] >= 'A' && input_text[i] <= 'Z'))
        {
            letters++;
        }
    }
    return letters;
}

int get_words(char input_text[], int len)
{
    int words = 0;
    for (int i = 0; i < len; i++)
    {
        if (input_text[i] == ' ')
        {
            words++;
        }
    }
    // + 1 to count the last word, assuming text isn't empty
    return words + 1;
}

int get_sentences(char input_text[], int len)
{
    int sentences = 0;
    for (int i = 0; i < len; i++)
    {
        if (input_text[i] == '.' || input_text[i] == '!' || input_text[i] == '?')
        {
            sentences++;
        }
    }
    return sentences;
}

int ColemanLiau_Idx(int letters, int words, int sentences)
{
    float L = ((float)letters / words) * 100;
    float S = ((float)sentences / words) * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);
    return index;
}

