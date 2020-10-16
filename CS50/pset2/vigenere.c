#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, string argv[]) 
{
    // Get the key and assure that it is argv[1] and is not digit
    if (argc > 2)
    {
        printf("You entered more than one argument !");
        return 1;
    } else if (argv[1]) 
    {
        string k = argv[1];
        for (int j = 0, v = strlen(k); j < v; j++)
        {
            if (isdigit(k[j]))
            {
                printf("Please don't write any non-alphabetical item !\n");
                return 1;
            }
        }
        
        // Get the plaintext
        string p = GetString(); 
        
        // initialize variable we need        
        int v = strlen(argv[1]);
        int j = 0;
        int l = 0;
        
        // Encypher and print cypher
        for (int i = 0, n = strlen(p); i < n ; i++)
                {
                     if (isalpha(p[i]))
                     {
                         j = (i - l) % v;
                         if (islower(p[i]))
                         {
                         
                             int keyNums[v];
                             if (isupper(k[j]))
                             {
                                keyNums[j] = argv[1][j] - 'A';
                                int c = ((p[i] - 97 + keyNums[j]) % 26) + 97;
                                printf("%c", c);
                             } else if (islower(k[j]))
                             {
                                keyNums[j] = argv[1][j] - 'a';
                                int c = ((p[i] - 97 + keyNums[j]) % 26) + 97;
                                printf("%c", c);
                             }
                        } else if (isupper(p[i]))
                            {
                            int keyNums[v]; 
                             if (isupper(k[j]))
                             {
                                keyNums[j] = argv[1][j] - 'A';
                                int c = ((p[i] - 65 + keyNums[j]) % 26) + 65;
                                printf("%c", c);
                             } else if (islower(k[j]))
                             {
                                 keyNums[j] = argv[1][j] - 'a';
                                int c = ((p[i] - 65 + keyNums[j]) % 26) + 65;
                                printf("%c", c);
                             }
                            }  
                     } else 
                         {
                            printf("%c", p[i]);
                             l++;
                         } 
                }
                printf("\n");
                return 0;  
    } else 
        printf("Your didn't entered an argument\n");
        return 1;
}