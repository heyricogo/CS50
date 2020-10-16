#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4 || (atoi(argv[1]) > 100 || atoi(argv[1]) < 1))
    {
        fprintf(stderr, "Usage: resize newSize infile outfile\n");
        return 1;
    }

    // remember filenames and the size to resize by.
    char *infile = argv[2];
    char *outfile = argv[3];
    int scale = atoi(argv[1]);

    // open input file and if it couldn't open throw an error.
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file and if it couldn't open throw an error.
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }
    // update width and height
    bi.biWidth *= scale;
    bi.biHeight *= scale;

    // determine padding for scanlines
    int resize_padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int padding = (4 - (bi.biWidth / scale * sizeof(RGBTRIPLE)) % 4) % 4;

    // set the bi an bf's sizes.
    bi.biSizeImage = ((3 * bi.biWidth) + resize_padding) * abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(bi.biHeight) / scale; i < biHeight; i++)
    {
        // creating an array of struct RGBTRIPLE that will hold the current scanline in it.
        RGBTRIPLE current_row[bi.biWidth];
        int position = 0;

        // iterate over pixels in scanline
        for (int j = 0; j < bi.biWidth / scale; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // iterate as many times as scale, draw the pixle and add it to the current_row array.
            for (size_t k = 0; k < scale; k++)
            {
                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                current_row[position] = triple;
                position++;
            }
        }

        // Add padding for the original scanlines.
        for (int k = 0; k < resize_padding; k++)
        {
            fputc(0x00, outptr);
        }

        if (scale != 1)
        {
            // add extra scanlines times scale - 1.
            for (int a = 0; a < scale - 1; a++)
            {
                // iterate over pixels in scanline
                for (int b = 0; b <  bi.biWidth; b++)
                {
                    fwrite(&current_row[b], sizeof(RGBTRIPLE), 1, outptr);
                }
                // Add padding for the new scanlines.
                for (int k = 0; k < resize_padding; k++)
                {
                    fputc(0x00, outptr);
                }
            }
        }

        // skip over padding, if any
        fseek(inptr, padding, SEEK_CUR);
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}