// Tema 1 - SDA - DAVID SILVIU - GRUPA 315CB
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define dim_url 50
#define linie_maxim 1024
#define max_pag 50

typedef struct page {
    int id;
    char url[dim_url];
    char *description;
} Page;

typedef struct nod {
    Page *pagina;
    struct nod* urmator;
} Nod;

typedef struct stiva {
    Nod *varf;
} Stiva;

typedef struct tab {
    int id;
    Page *paginaCurenta;
    Stiva *inapoi;
    Stiva *inainte;
    struct tab *anterior;
    struct tab *urmator;
} Tab;

typedef struct browser {
    Tab *santinela;
    Tab *curent;
    int ultim_id;
} Browser;

// Pagina
Page *creeaza_pagina(int id, char *url, char *description) {
    Page *p = malloc(sizeof(Page));
    p->id = id;
    strncpy(p->url, url, dim_url - 1);
    p->url[dim_url - 1] = '\0';
    p->description = strdup(description);
    return p;
}

void distruge_pagina(Page *p) {
    if (!p) return;
    free(p->description);
    free(p);
}

// Stiva
Stiva* creeaza_stiva() {
    Stiva *s = malloc(sizeof(Stiva));
    s->varf = NULL;
    return s;
}

void push(Stiva *s, Page *pagina) {
    Nod *n = malloc(sizeof(Nod));
    n->pagina = pagina;
    n->urmator = s->varf;
    s->varf = n;
}

Page *pop(Stiva *s) {
    if (!s->varf)
        return NULL;
    Nod* aux = s->varf;
    Page *p = aux->pagina;
    s->varf = aux->urmator;
    free(aux);
    return p;
}

int e_gol(Stiva* s) {
    return s->varf == NULL;
}

void curata_stiva(Stiva *s) {
    while (!e_gol(s)) {
        pop(s);
    }
}

void distruge_stiva(Stiva *s) {
    curata_stiva(s);
    free(s);
}

void afiseaza_stiva(Nod* nod) {
    if (!nod) return;
    afiseaza_stiva(nod->urmator);
    printf("%s\n", nod->pagina->url);
}

// Tab
Tab* creeaza_tab(int id, Page *pagina) {
    Tab *t = calloc(1, sizeof(Tab));
    t->id = id;
    t->paginaCurenta = pagina;
    t->inapoi = creeaza_stiva();
    t->inainte = creeaza_stiva();
    return t;
}

void distruge_tab(Tab *t) {
    distruge_stiva(t->inapoi);
    distruge_stiva(t->inainte);
    free(t);
}

// Browser
Browser *creeaza_browser(Page* pagina) {
    Browser *b = malloc(sizeof(Browser));
    Tab *s = calloc(1, sizeof(Tab));
    s->id = -1;
    s->urmator = s;
    s->anterior = s;
    b->santinela = s;

    Tab* t0 = creeaza_tab(0, pagina);
    t0->urmator = s;
    t0->anterior = s;
    s->urmator = t0;
    s->anterior = t0;

    b->curent = t0;
    b->ultim_id = 0;
    return b;
}

Tab *gaseste_tab(Browser *b, int id) {
    Tab *t = b->santinela->urmator;
    while (t != b->santinela) {
        if (t->id == id)
            return t;
        t = t->urmator;
    }
    return NULL;
}

void tab_nou(Browser *b, Page *pagina) {
    Tab *t = creeaza_tab(++b->ultim_id, pagina);
    Tab *last = b->santinela->anterior;
    last->urmator = t;
    t->anterior = last;
    t->urmator = b->santinela;
    b->santinela->anterior = t;
    b->curent = t;
}

void inchide_tab(Browser *b) {
    if (b->curent->id == 0) {
        printf("403 Forbidden\n");
        return;
    }
    Tab *de_sters = b->curent;
    de_sters->anterior->urmator = de_sters->urmator;
    de_sters->urmator->anterior = de_sters->anterior;
    b->curent = de_sters->anterior;
    distruge_tab(de_sters);
}

void afiseaza_tab(Browser *b) {
    Tab *t = b->curent;
    do {
        printf("%d ", t->id);
        if (t->urmator == b->santinela) {
            t = b->santinela->urmator;
        } else {
            t = t->urmator;
        }
    } while (t != b->curent);
    printf("\n");
    printf("%s", b->curent->paginaCurenta->description);
}

void afiseaza_istoric(Browser *b, int id) {
    Tab *t = gaseste_tab(b, id);
    if (!t) {
        printf("403 Forbidden\n");
        return;
    }
    afiseaza_stiva(t->inainte->varf);
    printf("%s\n", t->paginaCurenta->url);
    Nod *n = t->inapoi->varf;
    while (n) {
        printf("%s\n", n->pagina->url);
        n = n->urmator;
    }
}

void schimba_pagina(Browser *b, Page *p) {
    if (!p) {
        printf("403 Forbidden\n");
        return;
    }
    push(b->curent->inapoi, b->curent->paginaCurenta);
    curata_stiva(b->curent->inainte);
    b->curent->paginaCurenta = p;
}

void inapoi(Browser *b) {
    if (e_gol(b->curent->inapoi)) {
        printf("403 Forbidden\n");
        return;
    }
    push(b->curent->inainte, b->curent->paginaCurenta);
    b->curent->paginaCurenta = pop(b->curent->inapoi);
}

void inainte(Browser *b) {
    if (e_gol(b->curent->inainte)) {
        printf("403 Forbidden\n");
        return;
    }
    push(b->curent->inapoi, b->curent->paginaCurenta);
    b->curent->paginaCurenta = pop(b->curent->inainte);
}

int main() {
    int contor_pag;
    scanf("%d\n", &contor_pag);
    Page *pagini[max_pag];
    for (int i = 0; i < contor_pag; i++) {
        int id;
        char url[dim_url] = {0};
        char descriere[linie_maxim] = {0};

        scanf("%d\n", &id);
        memset(url, 0, dim_url);
        fgets(url, dim_url, stdin);
        url[strcspn(url, "\n")] = '\0';

        memset(descriere, 0, linie_maxim);
        fgets(descriere, linie_maxim, stdin);
        descriere[strcspn(descriere, "\n")] = '\0';
        strcat(descriere, "\n");

        pagini[i] = creeaza_pagina(id, url, descriere);
    }

    Page *pagina0 = creeaza_pagina(0, "https://acs.pub.ro/",
    "Computer Science\n");
    Browser *browser = creeaza_browser(pagina0);

    int n;
    scanf("%d\n", &n);
    char linie[linie_maxim];
    for (int i = 0; i < n; i++) {
        memset(linie, 0, linie_maxim);
        fgets(linie, linie_maxim, stdin);
        linie[strcspn(linie, "\n")] = '\0';
        if (strncmp(linie, "NEW_TAB", 7) == 0) {
            tab_nou(browser, pagina0);
        } else if (strncmp(linie, "CLOSE", 5) == 0) {
            inchide_tab(browser);
        } else if (strncmp(linie, "PRINT_HISTORY", 13) == 0) {
            int id;
            sscanf(linie + 14, "%d", &id);
            afiseaza_istoric(browser, id);
        } else if (strncmp(linie, "PRINT", 5) == 0) {
            afiseaza_tab(browser);
        } else if (strncmp(linie, "OPEN", 4) == 0) {
            int id;
            sscanf(linie + 5, "%d", &id);
            Tab* t = gaseste_tab(browser, id);
            if (!t)
                printf("403 Forbidden\n");
            else
                browser->curent = t;
        } else if (strncmp(linie, "PAGE", 4) == 0) {
            int id;
            sscanf(linie + 5, "%d", &id);
            Page* p = NULL;
            for (int j = 0; j < contor_pag; j++)
                if (pagini[j]->id == id) p = pagini[j];
            schimba_pagina(browser, p);
        } else if (strncmp(linie, "BACKWARD", 8) == 0) {
            inapoi(browser);
        } else if (strncmp(linie, "FORWARD", 7) == 0) {
            inainte(browser);
        } else if (strncmp(linie, "NEXT", 4) == 0) {
            if (browser->curent->urmator == browser->santinela) {
                browser->curent = browser->santinela->urmator;
            } else {
                browser->curent = browser->curent->urmator;
            }
        } else if (strncmp(linie, "PREV", 4) == 0) {
            if (browser->curent->anterior == browser->santinela) {
                browser->curent = browser->santinela->anterior;
            } else {
                browser->curent = browser->curent->anterior;
            }
        }
    }

    for (int i = 0; i < contor_pag; i++) {
        distruge_pagina(pagini[i]);
    }

    Tab *t = browser->santinela->urmator;
    while (t != browser->santinela) {
        Tab *urmator = t->urmator;
        distruge_tab(t);
        t = urmator;
    }
    free(browser->santinela);
    free(browser);
    distruge_pagina(pagina0);
    return 0;
}
