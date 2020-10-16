/**
 * Implements a dictionary's functionality.
 * Hashtable data structure
 */

#include <stdbool.h>
#include <stdio.h>
#include <strings.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

#include "dictionary.h"

#define HASHTABLE_SIZE 65536

// define struct node
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;


// declare words to count the words in the dictionary
int dic_size = 0;
// declare hashtable
node *hashtable[HASHTABLE_SIZE];

// hash funtion 
// using a hash function I found online : https://cs50.stackexchange.com/questions/18879/problems-with-hash-function-in-pset5
int hash(const char *word)
{
    unsigned int hash = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
        hash = (hash << 2) ^ word[i];
    return hash % HASHTABLE_SIZE;
}


/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    int len = strlen(word);
    char lword[len + 1];
    for (int i = 0; i < len; i++)
    {
        lword[i] = tolower(word[i]);
    }
    lword[len] = '\0';
    
    int bucket = hash(lword);
    node *cursor = hashtable[bucket];
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, lword) != 0)
            cursor = cursor->next;
        else
            return true;
    }
    return false;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    FILE *dic = fopen(dictionary, "r");
    if (dic == NULL)
    {
        fprintf(stderr, "Cound not open %s.\n", dictionary);
        return false;
    }
    
    char buffer[LENGTH + 1];
    
    while (fscanf(dic, "%s", buffer) != EOF)
    {
        // create a temporary node
        node *temp = calloc(1, sizeof(node));

        strncpy(temp->word, buffer, sizeof(buffer));
        
        // implement hash function to get the index
        int index = hash(buffer);
        
        // if the corresponding index in hashtable is empty, assign it to the temp node
        if (hashtable[index] == NULL)
            hashtable[index] = temp;

        // else append temp to the start of the linked list
        else
        {
            temp->next = hashtable[index];
            hashtable[index] = temp;
        }
        dic_size ++;
    }
    fclose(dic);
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    return dic_size;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    for (int i = 0; i < HASHTABLE_SIZE; i++)
    {
        node* cursor = hashtable[i];
         while (cursor != NULL)
            {
                node* temp = cursor;
                cursor = cursor->next;
                free(temp);
             }
            hashtable[i] = NULL;
    }
    return true;
}