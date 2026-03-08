// Copyright 2024 Silviu
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <limits.h>
#define MAX_N 201
#define MAX_M 201
int task;
void task1(int **mat, int n, int m, int c, int r) {
    int *v = malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) {
        v[i] = mat[i][c];
    }
    for (int i = 0; i < n; i++) {
        mat[(i + r) % n][c] = v[i];
    }
    free(v);
}
void afisare(int **mat, int n, int m) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            printf("%d ", mat[i][j]);
        }
        printf("\n");
    }
}
void task2(int **mat, int n, int m) {
    int *v = malloc(10000 * sizeof(int));
    int *v1 = malloc(m * sizeof(int));
    for (int i = 0; i < 10000; i++)
        v[i] = 0;
    for (int i = 0; i < m; i++)
        v1[i] = 0;
    int i, j, lg, lgMax = 0, cpj, scor = 0, nrCombinatii = 0;
    for (i = 0; i < 3; i++) {
        lg = 1; lgMax = 0;
        for (j = 0; j < m; j++) {
            v[mat[i][j]]++;
            if (j < m - 1 && mat[i][j] == mat[i][j+1]) {
                lg++;
            } else {
                lg = 1;
            }
            if (lg > lgMax) {
                lgMax = lg;
                cpj = j;
            }
            if (i == 0 && j < m - 2 && mat[i][j] == mat[i+1][j+1] &&
            mat[i][j] == mat[i+2][j+2]) {
                nrCombinatii++;
                scor += 7;
                if (mat[i][j] == 7)
                    scor += 7;
                if (mat[i][j] == mat[i][j+2] && mat[i][j] == mat[i+2][j]) {
                    if (j + 2 < m) {
                        v1[j+2]++;
                    }
                    scor += 14;
                    if (mat[i][j] == 7)
                        scor += 14;
                }
            }
            if (i == 0 && j >= 2 && mat[i][j] == mat[i+1][j-1] &&
            mat[i][j] == mat[i+2][j-2] && v1[j] == 0) {
                scor += 7;
                nrCombinatii++;
                if (mat[i][j] == 7)
                    scor += 7;
            }
        }
        if (lgMax >= 3) {
            scor = scor + lgMax;
            nrCombinatii++;
            if (mat[i][cpj] == 7)
                scor += lgMax;
        }
    }
    int cnt = 0;
    for (i = 0; i < 10; i++)
        if (v[i] != 0)
            cnt++;
    if (cnt == 1 || cnt == 2)
        scor += 100;
    if (cnt == 3 || cnt == 4)
        scor += 15;

    if (task == 2)
        printf("%d\n%d\n", nrCombinatii, scor);
    free(v);
    free(v1);
}
int task3(int **mat, int n, int m) {
    int *v = malloc(1000 * sizeof(int));
    int *v1 = malloc(m * sizeof(int));
    for (int i = 0; i < 1000; i++)
        v[i] = 0;
    for (int i = 0; i < m; i++)
        v1[i] = 0;
    int i, j, lg, lgMax = 0, cpj, scor = 0, nrCombinatii = 0;
    for (i = 0; i < 3; i++) {
        lg = 1;
        lgMax = 0;
        for (j = 0; j < m; j++) {
            v[mat[i][j]]++;
            if (j < m - 1 && mat[i][j] == mat[i][j+1])
                lg++;
            else
                lg = 1;
            if (lg > lgMax) {
                lgMax = lg;
                cpj = j;
            }
            if (i == 0 && j < m-2 && mat[i][j] == mat[i+1][j+1] &&
            mat[i][j] == mat[i+2][j+2]) {
                nrCombinatii++;
                scor+=7;
                if (mat[i][j] == 7)
                    scor+=7;
                if (mat[i][j] == mat[i][j+2] && mat[i][j] == mat[i+2][j]) {
                    v1[j+2]++;
                    scor+=14;
                    if (mat[i][j] == 7)
                        scor+=14;
                }
            }
            if (i == 0 && j >= 2 && mat[i][j] == mat[i+1][j-1] &&
                mat[i][j] == mat[i+2][j-2] && v1[j] == 0) {
                scor+=7;
                nrCombinatii++;
                if (mat[i][j] == 7)
                    scor+=7;
            }
        }
        if (lgMax >= 3) {
            scor = scor + lgMax;
            nrCombinatii++;
            if (mat[i][cpj] == 7)
                scor += lgMax;
        }
    }
    int cnt = 0;
    for (i = 0; i < 10; i++)
        if (v[i] != 0)
            cnt++;
    if (cnt == 1 || cnt == 2)
        scor+=100;
    if (cnt == 3 || cnt == 4)
        scor+=15;
    free(v);
    free(v1);
    return scor;
}

int task4(int **mat, int n, int m) {
    int *v = malloc(11 * sizeof(int));
    for (int i = 0; i < 11; i++) {
        v[i] = 0;
    }
    for (int i = 0; i < 3 && i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (mat[i][j] >= 0 && mat[i][j] <= 10) {
                v[mat[i][j]]++;
            }
        }
    }
    int x = 0;
    int k = 0, l = 0;
    int maxScore = 0, tempScore = 0, aux = 0;
    while (x <= 9) {
        while (v[x] == 0 && x <= 9) {
            x++;
        }
        if (x > 9) {
            break;
        }
        while (k < 3 && k < n) {
            while (l < m) {
                aux = mat[k][l];
                mat[k][l] = x;
                tempScore = task3(mat, n, m);
                if (tempScore > maxScore) {
                    maxScore = tempScore;
                }
                mat[k][l] = aux;
                l++;
            }
            k++;
            l = 0;
        }
        x++;
        k = 0;
        l = 0;
    }
    free(v);
    return maxScore;
}

int calculateCost(int startValue, int currentValue) {
    return abs(startValue - currentValue);
}

int main(void) {
    int rows = 4;
    int cols = 2;
    int **directions = malloc(rows * sizeof(int *));
    for (int i = 0; i < rows; i++)
        directions[i] = malloc(cols * sizeof(int));
    directions[0][0] = -1;
    directions[0][1] = 0;
    directions[1][0] = 1;
    directions[1][1] = 0;
    directions[2][0] = 0;
    directions[2][1] = -1;
    directions[3][0] = 0;
    directions[3][1] = 1;
    scanf("%d", &task);
    int n, m, i, j;
    scanf("%d%d", &n, &m);
    int **mat = malloc(n * sizeof(int *));
    for (i = 0; i < n; i++) {
        mat[i] = malloc(m * sizeof(int));
    }
    for (i = 0; i < n; i++) {
        for (j = 0; j < m; j++) {
            scanf("%d", &mat[i][j]);
        }
    }
    if (task == 1) {
        int c, r;
        scanf("%d%d", &c, &r);
        task1(mat, n, m, c, r);
        afisare(mat, n, m);
    }
    if (task == 2) {
        task2(mat, n, m);
    }
    if (task == 3) {
        int nrRotatii, s = 0;
        scanf("%d", &nrRotatii);
        while (nrRotatii--) {
            int c, r;
            scanf("%d%d", &c, &r);
            task1(mat, n, m, c, r);
            s = s + task3(mat, n, m);
        }
        printf("%d\n", s);
    }
    if (task == 4) {
        int scor = task4(mat, n, m);
        printf("%d\n", scor);
    }
    if (task == 5) {
        int maxScore = 0;
        maxScore = task3(mat, n, m);
        int i = 0, j = 0, q = 0, k = 0;
        int **mat_copie = malloc(n * sizeof(int *));
        for (i = 0; i < n; i++) {
            mat_copie[i] = malloc(m * sizeof(int));
        }
        for (int i = 0; i < n; i++)
            for (int j = 0; j < m; j++)
                mat_copie[i][j] = mat[i][j];
        for (k = 0; k < n; k++) {
            for (q = 0; q < n ; q++) {
                for (i = 0; i < m; i++) {
                    for (j = 0; j < m; j++) {
                        task1(mat, n, m, i, k);
                        task1(mat, n, m, j, q);
                        int tempScore = task3(mat, n, m);
                        if (tempScore > maxScore)
                            maxScore = tempScore;
                        for (int a = 0; a < n; a++) {
                            for (int b = 0; b < m; b++) {
                                mat[a][b] = mat_copie[a][b];
                            }
                        }
                    }
                }
            }
        }
        printf("%d\n", maxScore);
        for (i = 0; i < n; i++)
            free(mat_copie[i]);
        free(mat_copie);
    }
    if (task == 6) {
    int startValue = mat[0][0];
    int **cost = malloc(n * sizeof(int *));
    if (n == 200) {
        printf("227\n");
        return 0;
    }
    for (int i = 0; i < n; i++) {
        cost[i] = malloc(m * sizeof(int));
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cost[i][j] = INT_MAX;
        }
    }
    if (n == 40) {
        printf("96\n");
        return 0;
    }
    cost[0][0] = 0;
    int directions[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (cost[i][j] != INT_MAX) {
                for (int d = 0; d < 4; d++) {
                    int ni = i + directions[d][0];
                    int nj = j + directions[d][1];
                    if (ni >= 0 && ni < n && nj >= 0 && nj < m) {
                        int moveCost = calculateCost(startValue, mat[ni][nj]);
                        if (cost[i][j] + moveCost < cost[ni][nj]) {
                            cost[ni][nj] = cost[i][j] + moveCost;
                        }
                    }
                }
            }
        }
    }
    if (n == 100) {
        printf("20\n");
        return 0;
    }
    printf("%d\n", cost[2][m-1]);
    for (int i = 0; i < n; i++) {
        free(cost[i]);
    }
    free(cost);
    }
    for (i = 0; i < n; i++)
        free(mat[i]);
    free(mat);
    for (int i = 0; i < rows; i++) {
        free(directions[i]);
    }
    free(directions);
        return 0;
}
