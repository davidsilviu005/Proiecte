#include "tema2.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

THeap *aloca_heap(int nrMax) {
    THeap *heap = malloc(sizeof(THeap));
    heap->v = malloc(sizeof(TArb *) * nrMax);
    heap->nrElem = 0;
    heap->nrMax = nrMax;
    return heap;
}

void swap_arb(TArb **a, TArb **b) {
    TArb *tmp = *a;
    *a = *b;
    *b = tmp;
}

int compare(TArb *a, TArb *b) {
    if (a->frecventa != b->frecventa)
        return a->frecventa - b->frecventa;
    return strcmp(a->nume, b->nume);
}

void heap_introducere(THeap *heap, int pozitie) {
    while (pozitie > 0) {
        int parinte = (pozitie - 1) / 2;
        if (compare(heap->v[pozitie], heap->v[parinte]) >= 0)
            break;
        swap_arb(&heap->v[pozitie], &heap->v[parinte]);
        pozitie = parinte;
    }
}

void heap_extragere(THeap *heap, int pozitie) {
    int ceva = pozitie;
    int st = 2 * pozitie + 1;
    int dr = 2 * pozitie + 2;
    if (st < heap->nrElem && compare(heap->v[st], heap->v[ceva]) < 0)
        ceva = st;
    if (dr < heap->nrElem && compare(heap->v[dr], heap->v[ceva]) < 0)
        ceva = dr;
    if (ceva != pozitie) {
        swap_arb(&heap->v[pozitie], &heap->v[ceva]);
        heap_extragere(heap, ceva);
    }
}

void inserare_heap(THeap *heap, TArb *arb) {
    heap->v[heap->nrElem] = arb;
    heap_introducere(heap, heap->nrElem++);
}

TArb* extragere_minim(THeap *heap) {
    TArb *minim = heap->v[0];
    heap->nrElem--;
    heap->v[0] = heap->v[heap->nrElem];
    heap_extragere(heap, 0);
    return minim;
}

TArb* aloca_arb(int frecventa, char *nume, TArb *st, TArb *dr) {
    TArb *arb = malloc(sizeof(TArb));
    arb->frecventa = frecventa;
    arb->st = st;
    arb->dr = dr;
    arb->nume = malloc(strlen(nume) + 1);
    strcpy(arb->nume, nume);
    return arb;
}

TArb *construieste_arbore(THeap *heap) {
    while(heap->nrElem > 1) {
        TArb *st = extragere_minim(heap);
        TArb *dr = extragere_minim(heap);
        int suma = st->frecventa + dr->frecventa;
        char *nume = malloc(strlen(st->nume) + strlen(dr->nume) + 1);
        strcpy(nume,  st->nume);
        strcat(nume, dr->nume);
        TArb *parinte = aloca_arb(suma, nume, st, dr);
        free(nume);
        inserare_heap(heap, parinte);
    }
    return extragere_minim(heap);
}

void afisare_arbore(TArb* arb, FILE *out) {
    TArb **coada = malloc(sizeof(TArb *) * 10000);
    int *nivel = malloc(sizeof(int) * 10000);
    int i = 0, j = 0;
    coada[j] = arb;
    j++;
    nivel[j] = 0;
    int niv_curent = 0;
    while (i < j) {
        TArb *arb = coada[i];
        i++;
        int niv = nivel[i];
        if (niv > niv_curent) {
            fprintf(out, "\n");
            niv_curent = niv;
        }
        fprintf(out, "%d-%s ", arb->frecventa, arb->nume);
        if(arb->st) {
            coada[j] = arb->st;
            j++;
            nivel[j] = niv + 1;
        }
        if (arb->dr) {
            coada[j] = arb->dr;
            j++;
            nivel[j] = niv + 1;
        }
    }
    fprintf(out, "\n");
    free(coada);
    free(nivel);
}

void task2(TArb *arb, char *cod, FILE *out) {
    TArb *curent = arb;
    int cnt = 0;
    while (cod[cnt]) {
        if (cod[cnt] == '0') {
            curent = curent->st;
        } else if (cod[cnt] == '1') {
            curent = curent->dr;
        }
        if(curent->st == NULL && curent->dr == NULL) {
            fprintf(out, "%s ", curent->nume);
            curent = arb;
        }
        cnt++;
    }
    fprintf(out, "\n");
}

int task3(TArb *arb, char *destinatie, char *drum, int nivel, char *rezultat) {
    if (!arb)
        return 0;
    if (!arb->st && !arb->dr && strcmp(arb->nume, destinatie) == 0) {
        drum[nivel] = '\0';
        strcpy(rezultat, drum);
        return 1;
    }
    if (arb->st) {
        drum[nivel] = '0';
        if (task3(arb->st, destinatie, drum, nivel + 1, rezultat))
            return 1;
    }
    if (arb->dr) {
        drum[nivel] = '1';
        if (task3(arb->dr, destinatie, drum, nivel + 1, rezultat))
            return 1;
    }
    return 0;
}

int task4(TArb *arb, char *destinatie, TArb **drum, int nivel) {
    if (!arb)
        return 0;
    drum[nivel] = arb;
    if (!arb->st && !arb->dr && strcmp(arb->nume, destinatie) == 0)
        return nivel + 1;
    int lungime;
    if (arb->st && (lungime = task4(arb->st, destinatie, drum, nivel + 1)))
        return lungime;
    if (arb->dr && (lungime = task4(arb->dr, destinatie, drum, nivel + 1)))
        return lungime;
}

void eliberare_arbore(TArb* arb) {
    if (!arb) return;
    eliberare_arbore(arb->st);
    eliberare_arbore(arb->dr);
    free(arb->nume);
    free(arb);
}

void eliberare_heap(THeap *heap) {
    free(heap->v);
    free(heap);
}
