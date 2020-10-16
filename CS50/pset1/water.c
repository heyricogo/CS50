#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //Ask the question to the user
    int minutes;
    printf("minutes : ");
    minutes = GetInt();
    
    // calculate and print the number of bottle of water he waste 
    int bottles = 12 * minutes;
    printf("bottles: %d\n", bottles);
    
}