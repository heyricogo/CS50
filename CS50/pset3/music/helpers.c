// Helper functions for music

#include <cs50.h>
#include <string.h>
#include "helpers.h"
#include <math.h>


// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    char num = fraction[0]; // stores the value of the first character (i.e., the ASCII value of the first character)
    char denom = fraction[2]; // stores the value of the last character (i.e., the ASCII value of the last character)
    int numerator = num - 48; // stores the value of num converted to an int
    int denominator = denom - 48; // stores the value of denom converted to an int
    return (numerator * (8 / denominator));
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    float frequency;
    int longueur_note = strlen(note);
    char oct = note[longueur_note - 1];
    char note_letter = note[0];
    int octave = oct - 48;
    if (octave == 4)
    {
        frequency = 440;
    }
    else if (octave > 4)
    {
        frequency = round(440 * (2 * (octave - 4)));
    }
    else
    {
        frequency = round(440 / (2 * (4 - octave)));
    }
    if (longueur_note == 3)
    {
        char semitone = note[1];
        int test_semi_1 = semitone - 35;
        int test_semi_2 = semitone - 98;
        if (test_semi_1 == 0)
        {
            //frequency = frequency * pow(2,(1/12));
            frequency = frequency * pow(2.00, 1 / 12.00);
        }
        else if (test_semi_2 == 0)
        {
            frequency = frequency / pow(2.00, 1 / 12.00);
        }
    }
    switch (note_letter)
    {
        case 'A':
            break;
        case 'B':
            frequency = frequency * pow(2.00, 2 / 12.00);
            break;
        case 'C':
            frequency = frequency / pow(2.00, 9 / 12.00);
            break;
        case 'D':
            frequency = frequency / pow(2.00, 7 / 12.00);
            break;
        case 'E':
            frequency = frequency / pow(2.00, 5 / 12.00);
            break;
        case 'F':
            frequency = frequency / pow(2.00, 4 / 12.00);
            break;
        case 'G':
            frequency = frequency / pow(2.00, 2 / 12.00);
            break;
    }
    return round(frequency);
}


// Determines whether a string represents a rest
bool is_rest(string s)
{
    if (strcmp(s, "") == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}
