#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(void) 
{
    
    // prompt a user for their name
    string name = GetString();

    // output their initials in uppercase with no space foow by a newline
    printf("%c", toupper(name[0]));
    for (int i = 0, n = strlen(name); i < n; i++)
        {
            if (isspace(name[i]))
            {
                printf("%c", toupper(name[i+1]));
            }
        }
    printf("\n");
}