#include "chunk.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_1 32
#define MAX_2 4096
#define BITS_1 5
#define BITS_2 6
#define BITS_3 8
#define BAZA_1 0b111100000000
#define BAZA_2 0b000011111111
#define BAZA_3 0b00001111
#define BAZA_4 0b11111111
#define BAZA_5 0b00100000
#define BAZA_6 0b00011111

unsigned char* chunk_encode(char*** chunk, int width, int height, int depth, int* length) {
    int *v = malloc(width * height * depth * sizeof(int));
    unsigned char *v1 = malloc(height * depth * width * sizeof(unsigned char));
    int *v2 = malloc(width * height * depth * sizeof(int));
    int cnt = 0;
    int i = 0, j = 0, k = 0, lg = 1;
    for (i = 0; i < height; i++) {
        for (j = 0; j < depth; j++) {
            for (k = 0; k < width; k++) {
                v[cnt++] = chunk[k][i][j];
            }
        }
    }
    for (int i = 0; i < height * depth * width; i++)
        v1[i] = 0;
    j = 0;
    int x = v[0];
    for (i = 1; i < width * height * depth; i++) {
        if (v[i] != x) {
            v2[j++] = x;
            v2[j++] = lg;
            lg = 1;
            x = v[i];
        } else {
            lg++;
        }
    }
    v2[j++] = x;
    v2[j++] = lg;
    for (i = 0; i < j; i++) {
        v[i] = v2[i];
    }
    free(v2);
    k = 0;
    cnt = j;
    *(length) = 0;
    for (i = 0; i < cnt; i += 2) {
        int block = v[i];
        int numar = v[i + 1];
        v1[k] = 0;
        v1[k] |= (block << BITS_2);
        if (numar < MAX_1) {
            v1[k] |= numar;
        }
        if (numar >= MAX_1 && numar < MAX_2) {
            v1[k] |= MAX_1;
            int copie = numar;
            copie = ((numar & BAZA_1) >> BITS_3);
            v1[k] |= copie;
            int copie1 = (numar & BAZA_2);
            k++;
            v1[k] = 0;
            v1[k] |= copie1;
        } else {
            while (numar >= MAX_2) {
                v1[k] |= MAX_1;
                v1[k] |= BAZA_3;
                k++;
                v1[k] = BAZA_4;
                k++;
                numar -= (MAX_2 - 1);
            }
            if (numar < MAX_1) {
                v1[k] |= numar;
            }
            if (numar >= MAX_1 && numar < MAX_2) {
                v1[k] |= MAX_1;
                int copie = numar;
                copie = ((numar & BAZA_1) >> BITS_3);
                v1[k] |= copie;
                int copie1 = (numar & BAZA_2);
                k++;
                v1[k] = 0;
                v1[k] |= copie1;
            }
        }
        k++;
    }
    free(v);
    *(length) = k;
    return v1;
}



char*** chunk_decode(unsigned char* code, int width, int height, int depth) {
    char ***v = malloc(width * sizeof(char**));
    for (int i = 0; i < width; i++) {
        v[i] = malloc(height * sizeof(char*));
        for (int j = 0; j < height; j++) {
            v[i][j] = malloc(depth * sizeof(char));
            for (int k = 0; k < depth; k++) {
                v[i][j][k] = 0;
            }
        }
    }
    int cnt = 0;
    unsigned char v1 = 0, v2 = 0;
    int block = 0, lg = 0;
    for (int j = 0; j < height; j++) {
        for (int k = 0; k < depth; k++) {
            for (int i = 0; i < width; i++) {
                if (lg == 0) {
                    v1 = code[cnt++];

                    if ((v1 & BAZA_5) == 0) {
                        block = (v1 >> BITS_2);
                        lg = (v1 & BAZA_6);
                    } else {
                        block = (v1 >> BITS_2);
                        v2 = code[cnt++];
                        lg = ((v1 & BAZA_3) << BITS_3) | v2;
                    }
                }

                v[i][j][k] = (char)block;
                lg--;
            }
        }
    }

    return v;
}
