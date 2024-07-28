#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

const unsigned int N = 26;

node *table[N];

//             FAST, SLOW, DRAGON
typedef enum { DJB2, SDBM, LOSELOSE } HashAlgorithm;
HashAlgorithm selected_algorithm = DJB2;

unsigned int hash_djb2(const char *word);
unsigned int hash_sdbm(const char *word);
unsigned int hash_loselose(const char *word);

bool check(const char *word)
{
    char lower_word[LENGTH + 1];
    int i;
    for (i = 0; word[i] && i < LENGTH; i++)
    {
        lower_word[i] = tolower(word[i]);
    }
    lower_word[i] = '\0';

    unsigned int hash_value = hash(lower_word);

    for (node *cursor = table[hash_value]; cursor != NULL; cursor = cursor->next)
    {
        char lower_cursor_word[LENGTH + 1];
        for (i = 0; cursor->word[i] && i < LENGTH; i++)
        {
            lower_cursor_word[i] = tolower(cursor->word[i]);
        }
        lower_cursor_word[i] = '\0';

        if (strcmp(lower_word, lower_cursor_word) == 0)
        {
            return true;
        }
    }

    return false;
}


// Studying for this exercise I found this reference (http://www.cs.yorku.ca/~oz/hash.html),
// so I decided to implement all three proposed algorithms for exercise and for completeness of the solution.
unsigned int hash(const char *word)
{
    switch (selected_algorithm)
    {
        case DJB2:
            return hash_djb2(word) % N;
        case SDBM:
            return hash_sdbm(word) % N;
        case LOSELOSE:
            return hash_loselose(word) % N;
        default:
            return 0;
    }
}

unsigned int hash_djb2(const char *str)
{
    unsigned long hash = 5381;
    int c;
    while ((c = *str++))
    {
        hash = ((hash << 5) + hash) + c;
    }
    return hash;
}

unsigned int hash_sdbm(const char *str)
{
    unsigned long hash = 0;
    int c;
    while ((c = *str++))
    {
        hash = c + (hash << 6) + (hash << 16) - hash;
    }
    return hash;
}

unsigned int hash_loselose(const char *str)
{
    unsigned int hash = 0;
    int c;
    while ((c = *str++))
    {
        hash += c;
    }
    return hash;
}

bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];

    while (fscanf(file, "%45s", word) != EOF)
    {
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            fclose(file);
            return false;
        }

        strcpy(new_node->word, word);

        unsigned int hash_value = hash(word);

        new_node->next = table[hash_value];
        table[hash_value] = new_node;
    }

    fclose(file);
    return true;
}

unsigned int size(void)
{
    unsigned int count = 0;
    for (int i = 0; i < N; i++)
    {
        for (node *cursor = table[i]; cursor != NULL; cursor = cursor->next)
        {
            count++;
        }
    }
    return count;
}

bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}

