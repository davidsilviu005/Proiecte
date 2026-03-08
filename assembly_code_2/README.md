Task 1:
-Functia `sortari` sorteaza o lista simplu inlantuita de noduri in ordine crescatoare, fara a crea noduri noi. Parcurge nodurile date intr-un array si le leaga in ordine crescatoare, modificand direct pointerii next. Returneaza adresa noului cap al listei sortate.
Task 2:
-Functia `get_words` primeste un sir de caractere si il separa in cuvinte, folosind delimitatorii " .,\n". Pentru fiecare cuvant gasit, salveaza adresa acestuia in vectorul words. Se folosește functia standard strtok pentru impartirea sirului si se repeta pana se extrag toate cuvintele sau se atinge limita number_of_words.
-Functia `sort` sorteaza un vector de cuvinte (char** words) folosind qsort. Criteriul de sortare este: mai intai dupa lungimea cuvintelor, iar daca doua cuvinte au aceeasi lungime, se compara lexicografic. Compararea este realizata de functia compare, care folosește strlen si strcmp.
Task 3:
-Functia `kfib` calculeaza termenul de pe pozitia n dintr-un sir generalizat de tip Fibonacci, numit k-Fibonacci, unde fiecare termen este suma celor k termeni anteriori. Daca n este mai mic decat k, functia returneaza 0. Daca n este egal cu 1, intoarce 1. In celelalte cazuri, functia foloseste recursivitate pentru a calcula suma tuturor valorilor kfib(n - i, k) pentru fiecare i de la 1 la k. Valoarea finala este returnata in registrul eax.
Task 4:
-Functia `check_palindrome` verifica daca un sir de caractere este palindrom. Parcurge sirul simultan de la inceput si de la sfarsit, comparand caracterele corespunzatoare. Daca toate se potrivesc, returneaza 1. Daca gaseste o diferenta, intoarce 0.
-Functia `composite_palindrome` genereaza toate combinatiile posibile de concatenari de cuvinte dintr-o lista si verifica daca rezultatul este un palindrom. Daca gaseste un palindrom valid, retine cel mai lung sau, in caz de egalitate, cel mai mic lexicografic. Foloseste functii precum `check_palindrome`, `strlen`, `strcmp`, si `strdup`, iar rezultatul final este returnat ca string duplicat.
