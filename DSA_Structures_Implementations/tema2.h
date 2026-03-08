#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct TArb {
    int frecventa;
    char *nume;
    struct TArb *st, *dr;
} TArb;

typedef struct heap {
    TArb **v;
    int nrMax, nrElem;
} THeap;

THeap *aloca_heap(int nrMax);
void swap_arb(TArb **a, TArb **b);
int compare(TArb *a, TArb *b);
void heap_introducere(THeap *heap, int pozitie);
void heap_extragere(THeap *heap, int pozitie);
void inserare_heap(THeap *heap, TArb *arb);
TArb* extragere_minim(THeap *heap);
TArb* aloca_arb(int frecventa, char *nume, TArb *st, TArb *dr);
TArb *construieste_arbore(THeap *heap);
void afisare_arbore(TArb* arb, FILE *out);
void task2(TArb *arb, char *cod, FILE *out);
int task3(TArb *arb, char *destinatie, char *drum, int nivel, char *rezultat);
int task4(TArb *arb, char *destinatie, TArb **drum, int nivel);
void eliberare_arbore(TArb* arb);
void eliberare_heap(THeap *heap);