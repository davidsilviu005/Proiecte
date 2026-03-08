#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "functie.h"

int main() {
    int i;
    int **mat = (int **)malloc(7 * sizeof(int *));
    for (i = 1; i <= 7; i++) {
        mat[i] = (int *)malloc(7 * sizeof(int));
    }
    init(mat);
    int alege;
    printf("\e[1;1H\e[2J");
    printf("Alege cu cine vrei sa joci:\n1 - robot\n2 - alt jucator\nDecizia ta: ");
    scanf("%d", &alege);
    printf("\n");
    if (alege == 1) {
        int cine_incepe, cnt = 0, pozitie = 1;
        printf("1 - tu\n2 - calculatorul\n>=3 - aleator\nCine vrei sa inceapa primul: ");
        scanf("%d", &cine_incepe);
        printf("\e[1;1H\e[2J");
        printf("Tu vei fi 1 si vei avea culoarea albastru, iar adversarul tau va fi 2 si va avea culoarea rosie!\n");
        if (cine_incepe >= 3) {
            srand(time(NULL));
            cine_incepe = rand() % 2 + 1;
        }
        int e_ok = 1;
        while (check(mat) == 0) {
            if (cine_incepe == 1) {
numar1:
                e_ok = 1;
                if (cnt == 0 && cine_incepe == 1) {
                    printf("Uite asa arata tabla de joc, elementele vor cadea pe ultimul rand liber\n");
                    afisare(mat);
                }
                printf("Pe ce coloana vrei sa pui jetonul?(alege un numar de la 1 la 7): ");
                scanf("%d", &pozitie);
                printf("\n");
                punere_jucator(mat, pozitie, &e_ok);
                afisare(mat);
                if(e_ok == 0)
                    goto numar1;
                cine_incepe = 2;
                cnt++;
                if (verificare_jucator(mat)) {
                    printf("Felicitari! Ai castigat!\n");
                    //eliberare(mat);
                    return 0;
                }
            }
            if (cine_incepe == 2) {
                punere_robot(mat, cnt);
                afisare(mat);
                cine_incepe = 1;
                cnt++;
                if (verificare_robot(mat)) {
                    printf("Imi pare rau! Ai pierdut, poti incerca din nou.\n");
                    //eliberare(mat);
                    return 0;
                }
            }
        }
    } else if (alege == 2) {
        int cine_incepe, cnt = 0, pozitie = 1;
        printf("La inceput trebuie sa decideti cine va fi jucatorul 1 si jucatorului 2!\n");
        printf("1 - jucatorul 1\n2 - jucatorul 2\n>=3 - aleator\nCine vreti sa inceapa primul: ");
        scanf("%d", &cine_incepe);
        if (cine_incepe >= 3) {
            srand(time(NULL));
            cine_incepe = rand() % 2 + 1;
        }
        printf("\e[1;1H\e[2J");
        printf("Jucatorul numarul %d vei fi primul si vei va avea culoarea albastru, iar adversarul tau va avea culoarea rosie!\n\n", cine_incepe);
        int e_ok = 1;
        while (check(mat) == 0) {
            if (cine_incepe == 1) {
                if (cnt == 0) {
                    printf("Uite asa arata tabla de joc, elementele vor cadea pe ultimul rand liber\n");
                    afisare(mat);
                }
numar2:
                e_ok = 1;
                printf("Jucatorul 1, pe ce coloana vrei sa pui jetonul?(alege un numar de la 1 la 7): ");
                scanf("%d", &pozitie);
                printf("\n");
                punere_jucator(mat, pozitie, &e_ok);
                afisare(mat);
                if(e_ok == 0)
                    goto numar2;
                cine_incepe = 2;
                cnt++;
                if (verificare_jucator(mat)) {
                    printf("Felicitari! Jucatorul 1 a castigat!\n");
                    //eliberare(mat);
                    return 0;
                }
            }
            if (cine_incepe == 2) {
                if (cnt == 0) {
                    printf("Uite asa arata tabla de joc, elementele vor cadea pe ultimul rand liber\n");
                    afisare(mat);
                }
numar3:
                e_ok = 1;
                printf("Jucatorul 2, pe ce coloana vrei sa pui jetonul?(alege un numar de la 1 la 7): ");
                scanf("%d", &pozitie);
                printf("\n");
                jucator2(mat, pozitie, &e_ok);
                afisare(mat);
                if(e_ok == 0)
                    goto numar3;
                cine_incepe = 1;
                cnt++;
                if (verificare_robot(mat)) {
                    printf("Felicitari! Jucatorul 2 a castigat!\n");
                    //eliberare(mat);
                    return 0;
                }
            }
        }
    }
}
