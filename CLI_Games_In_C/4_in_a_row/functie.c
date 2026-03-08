#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "functie.h"

/*
define \e[1;1H\e[2J clear command prompt
define \033[0;30m black
define \033[0;31m red
define \033[0;32m green
define \033[0;33m yellow
define \033[0;34m blue
define \033[0;35m purple
define \033[0;36m cyan
define \033[0;37m white
define \033[0m reset_color    
*/

int check(int **mat) {
    for (int i = 1; i <= 7; i++) {
        if (mat[1][i] == 0)
            return 0;
    }
    return 1;
}

void eliberare(int **mat) {
    if (mat) {
        for (int i = 1; i <= 7; i++) {
            if(mat[i])
                free(mat[i]);
        }
        free(mat);
    }
}

void init(int **mat) {
    for (int i = 1; i <= 7; i++) {
        for (int j = 1; j <= 7; j++) {
            mat[i][j] = 0;
        }
    }
}

int verificare_jucator(int **mat) {
    for (int i = 1; i <= 7; i++) {
        for (int j = 1; j <= 4; j++) {
            if (mat[i][j] == 1 && mat[i][j + 1] == 1 && mat[i][j + 2] == 1 && mat[i][j + 3] == 1)
                return 1;
        }
    }
    for (int i = 4; i <= 7; i++) {
        for (int j = 1; j <= 4; j++) {
            if (mat[i][j] == 1 && mat[i - 1][j + 1] == 1 && mat[i - 2][j + 2] == 1 && mat[i - 3][j + 3] == 1)
                return 1;
        }
    }
    for (int i = 1; i <= 4; i++) {
        for (int j = 1; j <= 4; j++) {
            if (mat[i][j] == 1 && mat[i + 1][j + 1] == 1 && mat[i + 2][j + 2] == 1 && mat[i + 3][j + 3] == 1)
                return 1;
        }
    }
    for (int i = 1; i <= 4; i++) {
        for (int j = 1; j <= 7; j++) {
            if (mat[i][j] == 1 && mat[i + 1][j] == 1 && mat[i + 2][j] == 1 && mat[i + 3][j] == 1)
                return 1;
        }
    }
    return 0;
}

int verificare_robot(int **mat) {
    for (int i = 1; i <= 7; i++) {
        for (int j = 1; j <= 4; j++) {
            if (mat[i][j] == 2 && mat[i][j + 1] == 2 && mat[i][j + 2] == 2 && mat[i][j + 3] == 2)
                return 1;
        }
    }
    for (int i = 4; i <= 7; i++) {
        for (int j = 1; j <= 4; j++) {
            if (mat[i][j] == 2 && mat[i - 1][j + 1] == 2 && mat[i - 2][j + 2] == 2 && mat[i - 3][j + 3] == 2)
                return 1;
        }
    }
    for (int i = 1; i <= 4; i++) {
        for (int j = 1; j <= 4; j++) {
            if (mat[i][j] == 2 && mat[i + 1][j + 1] == 2 && mat[i + 2][j + 2] == 2 && mat[i + 3][j + 3] == 2)
                return 1;
        }
    }
    for (int i = 1; i <= 4; i++) {
        for (int j = 1; j <= 7; j++) {
            if (mat[i][j] == 2 && mat[i + 1][j] == 2 && mat[i + 2][j] == 2 && mat[i + 3][j] == 2)
                return 1;
        }
    }
    return 0;
}


void functie_robot(int **mat, int *pozi, int *pozj, int *e_ok) {
    for (int i = 1; i <= 7; i++) {
        for (int j = 1; j <= 4; j++) {
            if (mat[i][j] == 1 && mat[i][j + 1] == 1 && mat[i][j + 2] == 1 && mat[i][j + 3] == 0) {
                if (i < 7 && mat[i + 1][j + 3] != 0) {
                    *pozi = i;
                    *pozj = j + 3;
                    return;
                }
                if (i == 7) {
                    *pozi = i;
                    *pozj = j + 3;
                    return;
                }
            } else if (mat[i][j] == 1 && mat[i][j + 1] == 1 && mat[i][j + 2] == 0 && mat[i][j + 3] == 1) {
                if (i < 7 && mat[i + 1][j + 2] != 0) {
                    *pozi = i;
                    *pozj = j + 2;
                    return;
                }
                if (i == 7) {
                    *pozi = i;
                    *pozj = j + 2;
                    return;
                }
            } else if (mat[i][j] == 1 && mat[i][j + 1] == 0 && mat[i][j + 2] == 1 && mat[i][j + 3] == 1) {
                if (i < 7 && mat[i + 1][j + 1] != 0) {
                    *pozi = i;
                    *pozj = j + 1;
                    return;
                }
                if (i == 7) {
                    *pozi = i;
                    *pozj = j + 1;
                    return;
                }
            } else if (mat[i][j] == 0 && mat[i][j + 1] == 1 && mat[i][j + 2] == 1 && mat[i][j + 3] == 1) {
                if (i < 7 && mat[i + 1][j] != 0) {
                    *pozi = i;
                    *pozj = j;
                    return;
                    
                }
                if (i == 7) {
                    *pozi = i;
                    *pozj = j;
                    return;
                }
            }
        }
    }
    for (int i = 4; i <= 7; i++) {
        for (int j = 1; j <= 4; j++) {
            if (mat[i][j] == 1 && mat[i - 1][j + 1] == 1 && mat[i - 2][j + 2] == 1 && mat[i - 3][j + 3] == 0) {
                if (i < 7 && mat[i - 2][j + 3] != 0) {
                    *pozi = i - 3;
                    *pozj = j + 3;
                    return;
                }
                if (i == 7 && mat[i - 2][j + 3] != 0) {
                    *pozi = i - 3;
                    *pozj = j + 3;
                    return;
                }
            } else if (mat[i][j] == 1 && mat[i - 1][j + 1] == 1 && mat[i - 2][j + 2] == 0 && mat[i - 3][j + 3] == 1) {
                if (i < 7 && mat[i - 1][j + 2] != 0) {
                    *pozi = i - 2;
                    *pozj = j + 2;
                    return;
                }
                if (i == 7 && mat[i - 1][j + 2] != 0) {
                    *pozi = i - 2;
                    *pozj = j + 2;
                    return;
                }
            } else if (mat[i][j] == 1 && mat[i - 1][j + 1] == 0 && mat[i - 2][j + 2] == 1 && mat[i - 3][j + 3] == 1) {
                if (i < 7 && mat[i][j + 1] != 0) {
                    *pozi = i - 1;
                    *pozj = j + 1;
                    return;
                }
                if (i == 7 && mat[i][j + 1] == 0) {
                    *pozi = i - 1;
                    *pozj = j + 1;
                    return;
                }
            } else if (mat[i][j] == 0 && mat[i - 1][j + 1] == 1 && mat[i - 2][j + 2] == 1 && mat[i - 3][j + 3] == 1) {
                if (i < 7 && mat[i + 1][j] != 0) {
                    *pozi = i;
                    *pozj = j;
                    return;
                }
                if (i == 7) {
                    *pozi = i;
                    *pozj = j;
                    return;
                }
            }
        }
    }
    for (int i = 1; i <= 4; i++) {
        for (int j = 1; j <= 4; j++) {
            if (mat[i][j] == 1 && mat[i + 1][j + 1] == 1 && mat[i + 2][j + 2] == 1 && mat[i + 3][j + 3] == 0) {
                *pozi = i + 3;
                *pozj = j + 3;
                return;
            } else if (mat[i][j] == 1 && mat[i + 1][j + 1] == 1 && mat[i + 2][j + 2] == 0 && mat[i + 3][j + 3] == 1) {
                *pozi = i + 2;
                *pozj = j + 2;
                return;
            } else if (mat[i][j] == 1 && mat[i + 1][j + 1] == 0 && mat[i + 2][j + 2] == 1 && mat[i + 3][j + 3] == 1) {
                *pozi = i + 1;
                *pozj = j + 1;
                return;
            } else if (mat[i][j] == 0 && mat[i + 1][j + 1] == 1 && mat[i + 2][j + 2] == 1 && mat[i + 3][j + 3] == 1) {
                *pozi = i;
                *pozj = j;
                return;
            }
        }
    }
    for (int i = 7; i >= 4; i--) {
        for (int j = 1; j <= 7; j++) {
            if (mat[i][j] == 1 && mat[i - 1][j] == 1 && mat[i - 2][j] == 1 && mat[i - 3][j] == 0) {
                *pozi = i - 3;
                *pozj = j;
                return;
            }
        }
    }
    *e_ok = 0;
}

void verificare_castig_robot(int **mat, int *pozi, int *pozj) {
    for (int i = 1; i <= 7; i++) {
        for (int j = 1; j <= 4; j++) {
            if (mat[i][j] == 2 && mat[i][j + 1] == 2 && mat[i][j + 2] == 2 && mat[i][j + 3] == 0) {
                if (i < 7 && mat[i + 1][j + 3] != 0) {
                    *pozi = i;
                    *pozj = j + 3;
                    return;
                }
                if (i == 7) {
                    *pozi = i;
                    *pozj = j + 3;
                    return;
                }
            } else if (mat[i][j] == 2 && mat[i][j + 1] == 2 && mat[i][j + 2] == 0 && mat[i][j + 3] == 2) {
                if (i < 7 && mat[i + 1][j + 2] != 0) {
                    *pozi = i;
                    *pozj = j + 2;
                    return;
                }
                if (i == 7) {
                    *pozi = i;
                    *pozj = j + 2;
                    return;
                }
            } else if (mat[i][j] == 2 && mat[i][j + 1] == 0 && mat[i][j + 2] == 2 && mat[i][j + 3] == 2) {
                if (i < 7 && mat[i + 1][j + 1] != 0) {
                    *pozi = i;
                    *pozj = j + 1;
                    return;
                }
                if (i == 7) {
                    *pozi = i;
                    *pozj = j + 1;
                    return;
                }
            } else if (mat[i][j] == 0 && mat[i][j + 1] == 2 && mat[i][j + 2] == 2 && mat[i][j + 3] == 2) {
                if (i < 7 && mat[i + 1][j] != 0) {
                    *pozi = i;
                    *pozj = j;
                    return;
                }
                if (i == 7) {
                    *pozi = i;
                    *pozj = j;
                    return;
                }
            }
        }
    }
    for (int i = 4; i <= 7; i++) {
        for (int j = 1; j <= 4; j++) {
            if (mat[i][j] == 2 && mat[i - 1][j + 1] == 2 && mat[i - 2][j + 2] == 2 && mat[i - 3][j + 3] == 0) {
                if (mat[i - 2][j + 3] != 0) {
                    *pozi = i - 3;
                    *pozj = j + 3;
                    return;
                }
            } else if (mat[i][j] == 2 && mat[i - 1][j + 1] == 2 && mat[i - 2][j + 2] == 0 && mat[i - 3][j + 3] == 2) {
                if (mat[i - 1][j + 2] != 0) {
                    *pozi = i - 2;
                    *pozj = j + 2;
                    return;
                }
            } else if (mat[i][j] == 2 && mat[i - 1][j + 1] == 0 && mat[i - 2][j + 2] == 2 && mat[i - 3][j + 3] == 2) {
                if (mat[i][j + 1] != 0) {
                    *pozi = i - 1;
                    *pozj = j - 1;
                    return;
                }
            } else if (mat[i][j] == 0 && mat[i - 1][j + 1] == 2 && mat[i - 2][j + 2] == 2 && mat[i - 3][j + 3] == 2) {
                if (i < 7 && mat[i + 1][j] != 0) {
                    *pozi = i;
                    *pozj = j;
                    return;
                }
                if (i == 7) {
                    *pozi = i;
                    *pozj = j;
                    return;
                }
            }
        }
    }
    for (int i = 1; i <= 4; i++) {
        for (int j = 1; j <= 4; j++) {
            if (mat[i][j] == 2 && mat[i + 1][j + 1] == 2 && mat[i + 2][j + 2] == 2 && mat[i + 3][j + 3] == 0) {
                if (i < 4 && mat[i + 4][j + 3] != 0) {
                    *pozi = i + 3;
                    *pozj = j + 3;
                    return;
                }
                if (i == 4) {
                    *pozi = i + 3;
                    *pozj = j + 3;
                    return;
                }
            } else if (mat[i][j] == 2 && mat[i + 1][j + 1] == 2 && mat[i + 2][j + 2] == 0 && mat[i + 3][j + 3] == 2) {
                if (mat[i + 3][j + 2] != 0) {
                    *pozi = i + 2;
                    *pozj = j + 2;
                    return;
                }
            } else if (mat[i][j] == 2 && mat[i + 1][j + 1] == 0 && mat[i + 2][j + 2] == 2 && mat[i + 3][j + 3] == 2) {
                if (mat[i + 2][j + 1] != 0) {
                    *pozi = i + 1;
                    *pozj = j + 1;
                    return;
                }
            } else if (mat[i][j] == 0 && mat[i + 1][j + 1] == 2 && mat[i + 2][j + 2] == 2 && mat[i + 3][j + 3] == 2) {
                if (mat[i + 1][j] != 0) {
                    *pozi = i;
                    *pozj = j;
                    return;
                }
            }
        }
    }
    for (int i = 1; i <= 4; i++) {
        for (int j = 1; j <= 7; j++) {
            if (mat[i][j] == 0 && mat[i + 1][j] == 2 && mat[i + 2][j] == 2 && mat[i + 3][j] == 2) {
                *pozi = i;
                *pozj = j;
                return;
            }
        }
    }
}


void afisare(int **mat) {
    printf("\033[0;35m");
    printf("   1   2   3   4   5   6   7\n");
    printf("\033[0m");
    printf("\033[0;33m");
    printf(" -----------------------------\n");
    printf("\033[0m");
    printf(" ");
    for (int i = 1; i <= 7; i++) {
        for (int j = 1; j <= 7; j++) {
            printf("\033[0;33m");
            printf ("| ");
            printf("\033[0m");
            if (mat[i][j] == 1) {
                printf("\033[0;34m");
                printf("%d ", mat[i][j]);
                printf("\033[0m");
            } else if (mat[i][j] == 2) {
                printf("\033[0;31m");
                printf("%d ", mat[i][j]);
                printf("\033[0m");
            } else {
                printf("%d ", mat[i][j]);
            }
        }
        printf("\033[0;33m");
        printf("|");
        printf("\033[0m");
        if (i < 7) {
            printf("\033[0;33m");
            printf("\n ----+---+---+---+---+---+---+\n ");
            printf("\033[0m");
        }
    }
    printf("\033[0;33m");
    printf("\n -----------------------------\n");
    printf("\033[0m");
    printf("\033[0;35m");
    printf("   1   2   3   4   5   6   7\n\n\n");
    printf("\033[0m");
}

void punere_jucator(int **mat, int pozj,int *e_ok) {
    if (mat[1][pozj] != 0) {
        printf("Nu e bine! Coloana este plina, incearca din nou!\n");
        *e_ok = 0;
        return;
    }
    int i = 1;
    if (mat[i][pozj] == 0) {
            while (i <= 6 && mat[i + 1][pozj] == 0) {
                i++;
        }
    }
    mat[i][pozj] = 1;
}

void jucator2(int **mat, int pozj,int *e_ok) {
    if (mat[1][pozj] != 0) {
        printf("Nu e bine! Coloana este plina, incearca din nou!\n");
        *e_ok = 0;
        return;
    }
    int i = 1;
    if (mat[i][pozj] == 0) {
            while (i <= 6 && mat[i + 1][pozj] == 0) {
                i++;
        }
    }
    mat[i][pozj] = 2;
}

void punere_robot(int **mat, int cnt1) {
    if (cnt1 == 0 || cnt1 == 1) {
        if(mat[7][4] == 0) {
            mat[7][4] = 2;
        } else {
            mat[7][5] = 2;
        }
        return;
    } 
    int e_ok = 1;
    int cnt = 1;
    int pozi = 0,pozj = 0;
    verificare_castig_robot(mat, &pozi, &pozj);
    if (pozi != 0 && pozj != 0) {
        if (((pozi + 1) <= 7 && mat[pozi + 1][pozj] != 0)  || (pozi == 7)) {
            mat[pozi][pozj] = 2;
            return;
        }
    }
    pozi = 0;
    pozj = 0;
    functie_robot(mat, &pozi, &pozj, &e_ok);
    if ((pozi + 1) <= 7 &&  mat[pozi + 1][pozj] == 0 && pozi != 0 && pozj != 0) {
        e_ok = 0;
        cnt++;
    }
    if (e_ok == 1) {
        mat[pozi][pozj] = 2;
        pozi = 0;
        pozj = 0;
    } else {
retry:
        srand(time(NULL));
        int i = 1;
        int j = rand() % 8;
        if (j == 0 || j == pozj)
            j = rand() % 8;
        if (mat[i][j] != 0)
            goto retry;        
        while (i <= 6 && mat[i + 1][j] == 0) {
            i++;
        }
        mat[i][j] = 2;
    }
}
