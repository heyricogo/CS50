#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define BUFFERSIZE 512

int main(int argc, char *argv[])
{
    // check correct usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: recover file\n");
        return 1;
    }
    
    // remember filenames and the size to resize by.
    char *card_file = argv[1];
    
    // open input file and if it couldn't open throw an error.
    FILE *card = fopen(card_file, "r");
    if (card == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", card_file);
        return 2;
    }
    
    unsigned char buffer[BUFFERSIZE];
    int jpg_number = 0;
    //int i = 0;
    char filename[8];
    FILE* img = NULL;
    
    //iterate until the end of the file
    while(fread(&buffer, 1, BUFFERSIZE, card) == BUFFERSIZE)
    {
        //check if it is a jpg file
        if (buffer[0] == 0xff 
        && buffer[1] == 0xd8 
        && buffer[2] == 0xff 
        && (buffer[3] & 0xf0) == 0xe0)
        {
            //check if a file is already open
            if (img != NULL)
            {
                fclose(img);
                
            }
            sprintf(filename, "%03i.jpg", jpg_number);
            img = fopen(filename, "w");
            fwrite(&buffer, 1, BUFFERSIZE, img);
            jpg_number++;
        }
        else
        {
            if (img !=NULL)
            {
                fwrite(&buffer, 1, BUFFERSIZE, img);
            }
        }
    }
    
}