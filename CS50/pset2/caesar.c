#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, string argv[]) 
{
    if (argv[1])
    {
    int k = atoi(argv[1]);
    
    if (k >= 0)
        {
        string p = GetString();
        
        for (int i = 0, n = strlen(p); i < n; i++)
        {
            if (isalpha(p[i]))
            {
                if (islower(p[i]))
                {
                    int c = (p[i] - 97 + k) % 26;
                    printf("%c", c + 97);
                } else if (isupper(p[i]))
                {
                    int c = (p[i] - 65 + k) % 26;
                    printf("%c", c + 65);
                }
            } else 
                printf("%c", p[i]); 
        }
        printf("\n");
        return 0;    
        } else 
        {
            printf("Your entered a negative argument\n");
            return 1;    
        }
    } else 
    {
        printf("Your didn't entered an argument\n");
        return 1;
    }
}   