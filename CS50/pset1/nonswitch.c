#include <cs50.h>
#include <stdio.h>

int main(void)
{
    printf("Please enter an int between 1 and 10 : ");
    int number = GetInt();
    if (number >=1 && number <4)
    {
        printf("You entered a little int\n");
    } else if (number >=4 && number <8)
    {
        printf("You entered a medium int\n");
    } else if (number >=8 && number <=10)
    {
        printf("You entered a large int\n");
    } else 
    {
        printf("You entered a bad bad thing!\n");
    }
}