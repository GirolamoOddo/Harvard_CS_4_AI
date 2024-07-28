#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define FAT_BLOCK_SIZE 512
int is_jpeg_signature(uint8_t buffer[]);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    uint8_t buffer[FAT_BLOCK_SIZE];
    FILE *img = NULL;
    char filename[8];
    int  file_count = 0;
    int  found_jpeg = 0;

    while (fread(buffer, 1, sizeof(buffer), card) == sizeof(buffer))
    {
        if (is_jpeg_signature(buffer))
        {
            // Clarification on this strange check: it is used to spot the start and the end of an image
            // so if is the first jpg encounterd zero became one, if is the second close the image because
            // we are exploiting the HP of contiguos images allocation.
            if (found_jpeg)
            {
                fclose(img);
            }
            else
            {
                found_jpeg = 1;
            }

            sprintf(filename, "%03d.jpg", file_count);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                printf("Could not create %s.\n", filename);
                fclose(card);
                return 1;
            }

            file_count++;
        }

        if (found_jpeg)
        {
            fwrite(buffer, sizeof(uint8_t), sizeof(buffer), img);
        }
    }

    if (img != NULL)
    {
        fclose(img);
    }

    fclose(card);
    return 0;
}

int is_jpeg_signature(uint8_t buffer[])
{
    return buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0;
}
