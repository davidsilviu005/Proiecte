#include <stdio.h>
#include <stdlib.h>
#include <time.h>
void afisare(int **mat, int n) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            printf("%d ",mat[i][j]);
        }
        printf("\n");
    }
}

void afisare1 (char **mat, int n) {
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            printf("%c ",mat[i][j]);
        }
        printf("\n");
    }
}

int adaugare_2x1(int **mat, int width, int verificare) {
    int pozitie1, pozitie2, pozitie3, pozitie4;
    printf("Introdu pozitiile (x1,y1) unde vrei sa pui barca de dimensiune 2x1(sau pe vericala 1x2):");
    scanf("%d%d", &pozitie1, &pozitie2);
    printf("Introdu pozitiile (x2,y2) unde vrei sa pui barca de dimensiune 2x1(sau pe vericala 1x2):");
    scanf("%d%d", &pozitie3, &pozitie4);
    if ((pozitie1 == (pozitie3 - 1) && (pozitie2 == pozitie4)) || (pozitie1 == (pozitie3 + 1) && (pozitie2 == pozitie4)) || (pozitie1 == pozitie3 && pozitie2 == (pozitie4 + 1)) || (pozitie1 == pozitie3 && pozitie2 == (pozitie4 - 1))) {
        if(pozitie1 >= 0 && pozitie1 < width && pozitie2 >= 0 && pozitie2 < width && pozitie3 >= 0 && pozitie3 < width && pozitie4 >= 0 && pozitie4 < width) {
            mat[pozitie1][pozitie2] = 1;
            mat[pozitie3][pozitie4] = 1;
        }
    } else {
        printf("Nu au fost introduse dimensiunile bune, te rog ia jocul de la inceput!\n");
        verificare = 0;
    }
    return verificare;
}

int adaugare_3x1(int **mat, int width, int verificare) {
    int pozitie1, pozitie2, pozitie3, pozitie4, pozitie5, pozitie6;
    printf("Introdu pozitiile (x1,y1) unde vrei sa pui barca de dimensiune 3x1(sau pe vericala 1x3):");
    scanf("%d%d", &pozitie1, &pozitie2);
    printf("Introdu pozitiile (x2,y2) unde vrei sa pui barca de dimensiune 3x1(sau pe vericala 1x3):");
    scanf("%d%d", &pozitie3, &pozitie4);
    printf("Introdu pozitiile (x3,y3) unde vrei sa pui barca de dimensiune 3x1(sau pe vericala 1x3):");
    scanf("%d%d", &pozitie5, &pozitie6);
    if ((pozitie1 == pozitie3 && pozitie3 == pozitie5 && pozitie2 == (pozitie4 - 1) && pozitie2 == (pozitie6 - 2)) || 
        (pozitie1 == pozitie3 && pozitie3 == pozitie5 && pozitie2 == (pozitie4 + 1) && pozitie2 == (pozitie6 + 2)) ||
        (pozitie2 == pozitie4 && pozitie4 == pozitie6 && pozitie1 == (pozitie3 - 1) && pozitie1 == (pozitie5 - 2)) ||
        (pozitie2 == pozitie4 && pozitie4 == pozitie6 && pozitie1 == (pozitie3 + 1) && pozitie1 == (pozitie5 + 2))) {
        if(pozitie1 >= 0 && pozitie1 < width && pozitie2 >= 0 && pozitie2 < width && pozitie3 >= 0 && pozitie3 < width && pozitie4 >= 0 && pozitie4 < width && pozitie5 >= 0 && pozitie5 < width && pozitie6 >= 0 && pozitie6 < width) {
            if(mat[pozitie1][pozitie2] == 0 && mat[pozitie3][pozitie4] == 0 && mat[pozitie5][pozitie6] == 0){
                mat[pozitie1][pozitie2] = 1;
                mat[pozitie3][pozitie4] = 1;
                mat[pozitie5][pozitie6] = 1;
            } else {
                printf("Barcile se intercaleaza, ia-o de la inceput!\n");
                verificare = 0;
            }
        } else {
            printf("Pozitiile depasesc limitele, te rog ia jocul de la inceput!\n");
            verificare = 0;
        }
    } else {
        printf("Nu au fost introduse dimensiunile bune, te rog ia jocul de la inceput!\n");
        verificare = 0;
    }
    return verificare;
}

int adaugare_4x1(int **mat, int width, int verificare) {
    int pozitie1, pozitie2, pozitie3, pozitie4, pozitie5, pozitie6, pozitie7, pozitie8;
    printf("Introdu pozitiile (x1,y1) unde vrei sa pui barca de dimensiune 4x1(sau pe vericala 1x4):");
    scanf("%d%d", &pozitie1, &pozitie2);
    printf("Introdu pozitiile (x2,y2) unde vrei sa pui barca de dimensiune 4x1(sau pe vericala 1x4):");
    scanf("%d%d", &pozitie3, &pozitie4);
    printf("Introdu pozitiile (x3,y3) unde vrei sa pui barca de dimensiune 4x1(sau pe vericala 1x4):");
    scanf("%d%d", &pozitie5, &pozitie6);
    printf("Introdu pozitiile (x4,y4) unde vrei sa pui barca de dimensiune 4x1(sau pe vericala 1x4):");
    scanf("%d%d", &pozitie7, &pozitie8);
    if ((pozitie1 == pozitie3 && pozitie3 == pozitie5 && pozitie2 == (pozitie4 - 1) && pozitie2 == (pozitie6 - 2) && pozitie2 == (pozitie8 - 3)) || 
        (pozitie1 == pozitie3 && pozitie3 == pozitie5 && pozitie2 == (pozitie4 + 1) && pozitie2 == (pozitie6 + 2) && pozitie2 == (pozitie8 + 3)) ||
        (pozitie2 == pozitie4 && pozitie4 == pozitie6 && pozitie1 == (pozitie3 - 1) && pozitie1 == (pozitie5 - 2) && pozitie1 == (pozitie7 - 3)) ||
        (pozitie2 == pozitie4 && pozitie4 == pozitie6 && pozitie1 == (pozitie3 + 1) && pozitie1 == (pozitie5 + 2) && pozitie1 == (pozitie7 + 3))) {
        if(pozitie1 >= 0 && pozitie1 < width && pozitie2 >= 0 && pozitie2 < width && pozitie3 >= 0 && pozitie3 < width && pozitie4 >= 0 && pozitie4 < width && pozitie5 >= 0 && pozitie5 < width && pozitie6 >= 0 && pozitie6 < width && pozitie7 >= 0 && pozitie7 < width && pozitie8 >= 0 && pozitie8 < width) {
            if(mat[pozitie1][pozitie2] == 0 && mat[pozitie3][pozitie4] == 0 && mat[pozitie5][pozitie6] == 0 && mat[pozitie7][pozitie8] == 0) {
                mat[pozitie1][pozitie2] = 1;
                mat[pozitie3][pozitie4] = 1;
                mat[pozitie5][pozitie6] = 1;
                mat[pozitie7][pozitie8] = 1;
            } else {
                printf("Barcile se intercaleaza, ia-o de la inceput!\n");
                verificare = 0;
            }
        } else {
            printf("Pozitiile depasesc limitele, te rog ia jocul de la inceput!\n");
            verificare = 0;
        }
    } else {
        printf("Nu au fost introduse dimensiunile bune, te rog ia jocul de la inceput!\n");
        verificare = 0;
    }
    return verificare;
}

int adaugare_5x1(int **mat, int width, int verificare) {
    int pozitie1, pozitie2, pozitie3, pozitie4, pozitie5, pozitie6, pozitie7, pozitie8, pozitie9, pozitie10;
    printf("Introdu pozitiile (x1,y1) unde vrei sa pui barca de dimensiune 5x1(sau pe vericala 1x5):");
    scanf("%d%d", &pozitie1, &pozitie2);
    printf("Introdu pozitiile (x2,y2) unde vrei sa pui barca de dimensiune 5x1(sau pe vericala 1x5):");
    scanf("%d%d", &pozitie3, &pozitie4);
    printf("Introdu pozitiile (x3,y3) unde vrei sa pui barca de dimensiune 5x1(sau pe vericala 1x5):");
    scanf("%d%d", &pozitie5, &pozitie6);
    printf("Introdu pozitiile (x4,y4) unde vrei sa pui barca de dimensiune 5x1(sau pe vericala 1x5):");
    scanf("%d%d", &pozitie7, &pozitie8);
    printf("Introdu pozitiile (x5,y5) unde vrei sa pui barca de dimensiune 5x1(sau pe vericala 1x5):");
    scanf("%d%d", &pozitie9, &pozitie10);
    if ((pozitie1 == pozitie3 && pozitie3 == pozitie5 && pozitie2 == (pozitie4 - 1) && pozitie2 == (pozitie6 - 2) && pozitie2 == (pozitie8 - 3) && pozitie2 == (pozitie10 - 4)) || 
        (pozitie1 == pozitie3 && pozitie3 == pozitie5 && pozitie2 == (pozitie4 + 1) && pozitie2 == (pozitie6 + 2) && pozitie2 == (pozitie8 + 3) && pozitie2 == (pozitie10 + 4)) ||
        (pozitie2 == pozitie4 && pozitie4 == pozitie6 && pozitie1 == (pozitie3 - 1) && pozitie1 == (pozitie5 - 2) && pozitie1 == (pozitie7 - 3) && pozitie1 == (pozitie9 - 4)) ||
        (pozitie2 == pozitie4 && pozitie4 == pozitie6 && pozitie1 == (pozitie3 + 1) && pozitie1 == (pozitie5 + 2) && pozitie1 == (pozitie7 + 3) && pozitie1 == (pozitie9 - 4))) {
        if(pozitie1 >= 0 && pozitie1 < width && pozitie2 >= 0 && pozitie2 < width && pozitie3 >= 0 && pozitie3 < width && pozitie4 >= 0 && pozitie4 < width && pozitie5 >= 0 && pozitie5 < width && pozitie6 >= 0 && pozitie6 < width && pozitie7 >= 0 && pozitie7 < width && pozitie8 >= 0 && pozitie8 < width) {
            if(mat[pozitie1][pozitie2] == 0 && mat[pozitie3][pozitie4] == 0 && mat[pozitie5][pozitie6] == 0 && mat[pozitie7][pozitie8] == 0 && mat[pozitie9][pozitie10] == 0) {
                mat[pozitie1][pozitie2] = 1;
                mat[pozitie3][pozitie4] = 1;
                mat[pozitie5][pozitie6] = 1;
                mat[pozitie7][pozitie8] = 1;
                mat[pozitie9][pozitie10] = 1;
            } else {
                printf("Barcile se intercaleaza, ia-o de la inceput!\n");
                verificare = 0;
            }
        } else {
            printf("Pozitiile depasesc limitele, te rog ia jocul de la inceput!\n");
            verificare = 0;
        }
    } else {
        printf("Nu au fost introduse dimensiunile bune, te rog ia jocul de la inceput!\n");
        verificare = 0;
    }
    return verificare;
}

void generare_robot(int **mat, int width) {
    srand(time(NULL));
    int i = 0, j = 0;
    int x = rand() % 10;
    int y = rand() % 10;
    if (y == 9)
        y--;
    mat[x][y] = 1;
    mat[x][y+1] = 1;
    int cnt = 0;
    while (cnt == 0) {
        x = rand() % 10;
        y = rand() % 10;
        if (x >= 8)
            x-=2;
        if (mat[x][y] == 0 && mat[x + 1][y]==0 && mat[x + 2][y] == 0) {
            mat[x][y] = 1;
            mat[x + 1][y] = 1;
            mat[x + 2][y] = 1;
            cnt++;
        }
    }
    cnt = 0;
    while (cnt == 0) {
        x = rand() % 10;
        y = rand() % 10;
        if (y >= 8)
            y = 7;
        if (mat[x][y] == 0 && mat[x][y + 1]==0 && mat[x][y + 2] == 0) {
            mat[x][y] = 1;
            mat[x][y + 1] = 1;
            mat[x][y + 2] = 1;
            cnt++;
        }
    }
    cnt = 0;
    while (cnt == 0) {
        x = rand() % 10;
        y = rand() % 10;
        if (x >= 7)
            x = 6;
        if (mat[x][y] == 0 && mat[x + 1][y]==0 && mat[x + 2][y] == 0 && mat[x + 3][y] == 0) {
            mat[x][y] = 1;
            mat[x+1][y] = 1;
            mat[x+2][y] = 1;
            mat[x+3][y] = 1;
            cnt++;
        }
    }
    cnt = 0;
    while (cnt == 0) {
        x = rand() % 10;
        y = rand() % 10;
        if (y >= 7)
            y = 6;
        if (mat[x][y] == 0 && mat[x][y + 1]==0 && mat[x][y + 2] == 0 && mat[x][y + 3] == 0 && mat[x][y+4] == 0) {
            mat[x][y] = 1;
            mat[x][y + 1] = 1;
            mat[x][y + 2] = 1;
            mat[x][y + 3] = 1;
            mat[x][y + 4] = 1;
            cnt++;
        }
    }
}

void incercare_robot(int **mat, int **mat1, int width, int *scor) {
    srand(time(NULL));
    int x = rand() % 10;
    int y = rand() % 10;
    if (mat1[x][y] == 1) {
        (*scor) += 1;
        mat[x][y] = 1;
    } else
        mat[x][y] = 8;
}

void incercare_player(int **mat, int **mat1, int width, int *scor) {
    int x = 0, y = 0;
    printf("Introdu coordonatele unde vrei sa tragi:");
    scanf("%d%d", &x, &y);
    int cnt = 0;
    if (mat1[x][y] == 1) {
        mat[x][y] = 1;
        (*scor) += 1;
    } else
        mat[x][y] = 8;
}

int main() {
    int width = 0;
    printf("Introdu dimensiunea(n x n) pe care vrei sa o aiba tabla de joc: ");
    scanf("%d", &width);
    int **mat1, **mat2;
    mat1 = (int **)malloc(width * sizeof(int *));
    for (int i = 0; i <= width; i++) {
        mat1[i] = (int *)malloc((width + 1) * sizeof(int));
    }
    mat2 = (int **)malloc(width * sizeof(int *));
    for (int i = 0; i <= width; i++) {
        mat2[i] = (int *)malloc((width + 1) * sizeof(int));
    }
    int i, j;
    for (i = 0; i <= width; i++) {
        for (j = 0; j <= width; j++) {
            mat1[i][j] = 0;
            mat2[i][j] = 0;
        }
    }
    
    int verificare = 1;
    verificare = adaugare_2x1(mat1, width, verificare);
    if (verificare == 0)
        return 0;
    printf("Matricea arata asa: \n");
    afisare(mat1, width);
    printf("Acum sa facem prima barca de dimensiune 3x1: \n");
    verificare = adaugare_3x1(mat1, width, verificare);
    if (verificare == 0)
        return 0;
    printf("Matricea arata asa: \n");
    afisare(mat1, width);
    printf("Acum sa facem a doua barca de dimensiune 3x1: \n");
    verificare = adaugare_3x1(mat1, width, verificare);
    if (verificare == 0)
        return 0;
    printf("Matricea arata asa: \n");
    afisare(mat1, width);
    verificare = adaugare_4x1(mat1, width, verificare);
    if (verificare == 0)
        return 0;
    printf("Matricea arata asa: \n");
    afisare(mat1, width);
    verificare = adaugare_5x1(mat1, width, verificare);
    if (verificare == 0)
        return 0;
    printf("Matricea arata asa: \n");
    afisare(mat1, width);
    generare_robot(mat2, width);

    //Incepere joc

    int scor1 = 0, scor2 = 0;
    int **mat_incercare1, **mat_incercare2;
    mat_incercare1 = (int **)malloc(width * sizeof(int *));
    for (int i = 0; i < width; i++) {
        mat_incercare1[i] = (int *)malloc(width * sizeof(int));
    }
    mat_incercare2 = (int **)malloc(width * sizeof(int *));
    for (int i = 0; i < width; i++) {
        mat_incercare2[i] = (int *)malloc(width * sizeof(int));
    }
    for (i = 0; i < width; i++) {
        for (j = 0; j < width; j++) {
            mat_incercare1[i][j] = 0;
            mat_incercare2[i][j] = 0;
        }
    }

    int cine_incepe = 0;
    printf("Cine vrei sa inceapa primul?(1 - tu, 2 - calculatorul, 3 - aleator): ");
    scanf("%d", &cine_incepe);
    printf("\n");
    if (cine_incepe == 3) {
        srand(time(NULL));
        cine_incepe = rand() % 2 + 1;
    }
    while (scor1 < 17 && scor2 < 17) {
        if (cine_incepe == 1) {
            incercare_player(mat_incercare1, mat2, width, &scor1);
            cine_incepe = 2;
        } else if (cine_incepe == 2) {
            incercare_robot(mat_incercare2, mat1, width, &scor2);
            cine_incepe = 1;
        } else {
            printf("Nu ai ales cat trebuie, ia-o de la inceput!");
            return 0;
        }
        afisare(mat_incercare1, width);
        printf("-------------------\n");
        afisare(mat_incercare2, width);
        printf("\n\n\n");
    }
    if (scor1 == 17)
        printf("Ai castigat!\n");
    if (scor2 == 17)
        printf("Ai pierdut!\n");

    for (int i = 0; i < width; i++) {
        free(mat_incercare1[i]);
        free(mat_incercare2[i]);
        free(mat1[i]);
        free(mat2[i]);
    }
    free(mat_incercare1);
    free(mat_incercare2);
    free(mat1);
    free(mat2);
    return 0;
}
