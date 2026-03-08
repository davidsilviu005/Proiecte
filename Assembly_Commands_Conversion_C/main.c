//DAVID SILVIU - GRUPA 315CB -> TEMA 1 - PCLP2
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int numar(char *s) {
	for (int i = 0; s[i] != '\0' && s[i] != ';'; i++) {
		if (s[i] < '0' || s[i] > '9')
			return 0;
	}
	return 1;
}

void afisare(char *s) {
	for (int i = 0; s[i] != '\0' && s[i] != ';'; i++)
		printf("%c", s[i]);
}

int stergere_indetare(char *p) {
	int i = 0;
	while (p[i] == '\t')
		i++;
	return i;
}

void afisare_egalare_variabila(char *varname, int *val) {
	if (strcmp(varname, "a") == 0)
		*val = 0;
	else if (strcmp(varname, "b") == 0)
		*val = 1;
	else if (strcmp(varname, "c") == 0)
		*val = 2;
	else if (strcmp(varname, "d") == 0)
		*val = 3;
}

void afisare_egalare_valoare(char *varname, int value) {
	if (strcmp(varname, "a") == 0)
		printf("MOV eax, %d\n", value);
	else if (strcmp(varname, "b") == 0)
		printf("MOV ebx, %d\n", value);
	else if (strcmp(varname, "c") == 0)
		printf("MOV ecx, %d\n", value);
	else if (strcmp(varname, "d") == 0)
		printf("MOV edx, %d\n", value);
}

void or(char *varname, char *p) {
	p = strtok(NULL, " ");
	if (numar(p)) {
		printf("OR e%sx, ", varname);
		afisare(p);
		printf("\n");
	} else {
		printf("OR e%sx, e%cx\n", varname, p[0]);
	}
}

void xor(char *varname, char *p) {
	p = strtok(NULL, " ");
	if (numar(p)) {
		printf("XOR e%sx, ", varname);
		afisare(p);
		printf("\n");
	} else {
		printf("XOR e%sx, e%cx\n", varname, p[0]);
	}
}

void and(char *varname, char *p) {
	p = strtok(NULL, " ");
	if (numar(p)) {
		printf("AND e%sx, ", varname);
		afisare(p);
		printf("\n");
	} else {
		printf("AND e%sx, e%cx\n", varname, p[0]);
	}
}

void add(char *varname, char *p) {
	p = strtok(NULL, " ");
	if (numar(p)) {
		printf("ADD e%sx, ", varname);
		afisare(p);
		printf("\n");
	} else {
		printf("ADD e%sx, e%cx\n", varname, p[0]);
	}
}

void sub(char *varname, char *p) {
	p = strtok(NULL, " ");
	if (numar(p)) {
		printf("SUB e%sx, ", varname);
		afisare(p);
		printf("\n");
	} else {
		printf("SUB e%sx, e%cx\n", varname, p[0]);
	}
}

void shr(char *varname, char *p) {
	p = strtok(NULL, " ");
	printf("SHR e%sx, ", varname);
	afisare(p);
	printf("\n");
}

void shl(char *varname, char *p) {
	p = strtok(NULL, " ");
	printf("SHL e%sx, ", varname);
	afisare(p);
	printf("\n");
}

void inmultire(char *varname, char *p) {
	printf("MOV eax, e%sx\n", varname);
	if (numar(p)) {
		printf("MUL ");
		afisare(p);
		printf("\n");
	} else {
		printf("MUL e");
		afisare(p);
		printf("x\n");
	}
	printf("MOV e%sx, eax\n", varname);
}

void impartire(char *varname, char *p) {
	printf("MOV eax, e%sx\n", varname);
	if (numar(p)) {
		printf("DIV ");
		afisare(p);
		printf("\n");
	} else {
		printf("DIV e");
		afisare(p);
		printf("x\n");
	}
	printf("MOV e%sx, eax\n", varname);
}

void verificare(char *varname) {
	if (strstr(varname, ">="))
		printf("JL end_label\n");
	else if (strstr(varname, "<="))
		printf("JG end_label\n");
	else if (strstr(varname, "=="))
		printf("JNE end_label\n");
	else if (strcmp(varname, ">") == 0)
		printf("JLE end_label\n");
	else if (strcmp(varname, "<") == 0)
		printf("JGE end_label\n");
}

void afisare_if(char *p, char *varname) {
	printf("CMP ");
	p = strtok(NULL, " ");
	printf("e%cx, ", p[1]);
	p = strtok(NULL, " ");
	strcpy(varname, p);
	p = strtok(NULL, " ");
	int value = atoi(p);
	printf("%d\n", value);
	verificare(varname);
}

void afisare_while(char *p, char *varname) {
	printf("start_loop:\n");
	p = strtok(NULL, " ");
	strcpy(varname, p + 1);
	printf("CMP e%sx, ", varname);
	p = strtok(NULL, " ");
	strcpy(varname, p);
	p = strtok(NULL, " ");
	int value = atoi(p);
	printf("%d\n", value);
	verificare(varname);
}

void afisare_for(char *p, char *varname) {
	p = strtok(NULL, " ");
	strcpy(varname, p + 1);
	printf("MOV e%sx, 0\nstart_loop:\n", varname);
	p = strtok(NULL, " ");
	p = strtok(NULL, " ");
	p = strtok(NULL, " ");
	p = strtok(NULL, " ");
	printf("CMP e%sx, ", varname);
	strcpy(varname, p);
	p = strtok(NULL, " ");
	int value = atoi(p);
	printf("%d\n", value);
	verificare(varname);
}

void indentare(char *s) {
	if (s[0] == '\t') {
		char *aux = malloc(20 * sizeof(char));
		strcpy(aux, s + 1);
		strcpy(s, aux);
		free(aux);
	}
}

void impartire_total(char *p, char *varname) {
	p = strtok(NULL, " ");
	int value = atoi(p);
	if (strstr(p, "0") && value == 0)
		printf("Error\n");
	else
		impartire(varname, p);
}

void inmultire_a(char *p) {
	printf("MUL ");
	afisare(p);
	printf("\n");
}

void afisare_sf(char *s1, char *varname, int este_if_while_for) {
	if (strstr(varname, "}") && este_if_while_for == 2)
		printf("JMP start_loop\nend_label:\n");
	else if (strstr(varname, "}") && este_if_while_for == 3)
		printf("ADD e%cx, 1\nJMP start_loop\nend_loop:\n", s1[0]);
	else if (strstr(varname, "}"))
		printf("end_label:\n");
}

int este_if_while_for;
int main(void) {
	char *s1 = malloc(1000 * sizeof(char));
	char *s = malloc(10000 * sizeof(char));
	while (fgets(s, 10000, stdin)) {
		if (strstr(s, "for"))
			strcpy(s1, s + 5);
		int beculetz = 1;
		int test = strlen(s);
		char *p = strtok(s, " ");
		char *varname = p;
		indentare(s);
		const char *reg[4] = {"eax", "ebx", "ecx", "edx"};
		if (strstr(varname, "}")) {
			afisare_sf(s1, varname, este_if_while_for);
			beculetz = 0;
		}
		if (test <= 9 && beculetz == 1) {
			p = strtok(NULL, " ");
			p = strtok(NULL, " ");
			int value = atoi(p);
			if (numar(p)) {
				afisare_egalare_valoare(varname, value);
			} else {
				int val = -1;
				afisare_egalare_variabila(varname, &val);
				if (val != -1) {
					int ceva = p[0] - 'a';
					if (ceva >= 0 && ceva < 4)
						printf("MOV %s, %s\n", reg[val], reg[ceva]);
				}
			}
		} else if (beculetz == 1) {
			if (s[0] == 'a' || s[0] == 'b' || s[0] == 'c' ||
				s[0] == 'd' || s[0] == ' ') {
				p = strtok(NULL, " ");
				p = strtok(NULL, " ");
				p = strtok(NULL, " ");
				if (*p == '^') {
					xor(varname, p);
				} else if (*p == '&') {
					and(varname, p);
				} else if (*p == '|') {
					or(varname, p);
				} else if (*p == '+') {
					add(varname, p);
				} else if (*p == '-') {
					sub(varname, p);
				} else if (*p == '*') {
					p = strtok(NULL, " ");
					if (strcmp(varname, "a") == 0) {
						inmultire_a(p);
						continue;
					}
					inmultire(varname, p);
				} else if (*p == '/') {
					impartire_total(p, varname);
				} else if (strcmp(p, ">>") == 0) {
					shr(varname, p);
				} else if (strcmp(p, "<<") == 0) {
					shl(varname, p);
				}
			} else {
				if (strstr(p, "if")) {
					afisare_if(p, varname);
				} else if (strstr(p, "while")) {
					este_if_while_for = 2;
					afisare_while(p, varname);
				} else if (strstr(p, "for")) {
					este_if_while_for = 3;
					afisare_for(p, varname);
				}
			}
		}
	}
	free(s);
	free(s1);
	return 0;
}
