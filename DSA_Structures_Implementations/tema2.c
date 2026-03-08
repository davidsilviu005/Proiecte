#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tema2.h"

int main(int argc, char *argv[]) {
    FILE *in = fopen(argv[2], "r");
    FILE *out = fopen(argv[3], "w");
    int n;
    fscanf(in, "%d", &n);
    THeap *heap = aloca_heap(n);
    for (int i = 0; i < n; i++) {
        int frecventa;
        char nume[15];
        fscanf(in, "%d %s", &frecventa, nume);
        inserare_heap(heap, aloca_arb(frecventa, nume, NULL, NULL));
    }
    TArb *arb = construieste_arbore(heap);
    if (strcmp(argv[1], "-c1") == 0) {
        afisare_arbore(arb, out);
    } else if (strcmp(argv[1], "-c2") == 0) {
        int x;
        fscanf(in , "%d", &x);
        char buffer[1024];
        for (int i = 0; i < x; i++) {
            fscanf(in, "%s", buffer);
            task2(arb, buffer, out);
        }
    } else if (strcmp(argv[1], "-c3") == 0) {
        int x;
        fscanf(in, "%d", &x);
        char nume[15];
        char drum[1000], rezultat[1000];
        for (int i = 0; i < x; i++) {
            fscanf(in,"%s", nume);
            if (task3(arb, nume, drum, 0, rezultat)) {
                fprintf(out, "%s", rezultat);
            }
        }
    } else if (strcmp(argv[1], "-c4") == 0) {
        int x;
        fscanf(in, "%d", &x);
        TArb *drum[x][1000];
        int lungime[x];
        char nume[15];
        for (int i = 0; i < x; i++) {
            fscanf(in, "%s", nume);
            lungime[i] = task4(arb, nume, drum[i], 0);
        }
        int nivel = 0;
        while(1) {
            int ceva = 1;
            for (int i = 1; i < x; i++) {
                if (nivel >= lungime[i] || drum[i][nivel] != drum[0][nivel]) {
                    ceva = 0;
                    break;
                }
            }
            if (!ceva)
                break;
            nivel++;
        }
        fprintf(out,"%s\n", drum[0][nivel - 1]->nume);
    }

    eliberare_arbore(arb);
    eliberare_heap(heap);
    fclose(in);
    fclose(out);
    return 0;
}