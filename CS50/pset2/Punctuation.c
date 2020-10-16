#include <stdio.h>
#include <string.h>
#include <cs50.h>
#include <ctype.h>

int main(void)
{
    string Text = "";
    int n = strlen(Text);
    do {
        Text = GetString();
    } while (n < 0 || n > 300);
    
    for (int i = 0; i < n; i++)
    {
        if (Text[i] == ",")
            {
            int c = ", ";
            printf("%c", c);
        } else if (Text[i] == ".")
            {
            int c = ". ";
            printf("%c", c);
            int d = Text[i + 1] - 32;
            printf("%c", d);
            i++;
        } else
        {
            int c = Text[i];
            printf("%c", c);
        }
    }
}
