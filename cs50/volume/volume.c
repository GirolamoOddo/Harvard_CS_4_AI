// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file
    int8_t buffer[HEADER_SIZE];
    fread( buffer, sizeof(buffer), 1,   input);
    fwrite(buffer , 1, sizeof(buffer), output);

    // TODO: Read samples from input file and write updated data to output file

    int16_t sound_chunck;
    while (fread(&sound_chunck, sizeof(sound_chunck), 1, input))
    {
        sound_chunck *= factor;
        fwrite(&sound_chunck, 1, sizeof(sound_chunck), output);
    }

    // Close files
    fclose(input);
    fclose(output);
}
