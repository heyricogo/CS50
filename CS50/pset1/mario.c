#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height = 0;
    //ask for the height of the piramid to the user
    do
    {
        printf("Height : ");
        height = get_int();
    } while (height < 0 || height > 23);
    // draw the piramid
   for(int i = 1; i < height + 1; i++)
   {
        for (int k=0;k<height-i;k++)
        {
            printf(" ");
        }
        for (int j=0;j<1+i;j++)
       {
           printf("#");
       }
       printf("\n");
   }
}