#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    // variables
    float change_owed = -1.0;
    int coins_used = 0;
    
    //Ask the user how much change is owed
    do
    {
        printf("O hai! How much change is owed?\n");
        change_owed = get_float();
    } while (change_owed <= 0);
    
    //spits out the minimum number of coins
    change_owed = change_owed * 100; // convert the user's input to cents
    change_owed = round(change_owed);   // round it to avoid mistakes
    
    // How many dollars ?
    coins_used += (int)change_owed / 100;
    change_owed = (int)change_owed % 100;
    
    // How many quarters ?
    coins_used += (int)change_owed / 25;
    change_owed = (int)change_owed % 25;
    
    // How many dimes ?
    coins_used += (int)change_owed / 10;
    change_owed = (int)change_owed % 10;
    
    // How many nickels ?
    coins_used += (int)change_owed / 5;
    change_owed = (int)change_owed % 5;
    
    // How many cents ?
    coins_used += (int)change_owed / 1;
    change_owed = (int)change_owed % 1;
    
    // How many coins ?
    printf("%d\n", coins_used);
}