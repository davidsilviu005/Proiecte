section .data
;pentru declararea delimitatorilor
delimitatori db " .,", 10, 0

section .text
global sort
global get_words
extern strtok
extern strlen
extern strcmp
extern qsort

;; get_words(char *s, char **words, int number_of_words)
;  separa stringul s in cuvinte si salveaza cuvintele in words
;  number_of_words reprezinta numarul de cuvinte
get_words:
    ; create a new stack frame
    enter 4, 0
    ;[ebp-4] = 0
    mov dword [ebp-4], 0
    push delimitatori
    ;pusham pe stiva [ebp+8] pentru a apela functia strtok
    push dword [ebp+8]
    call strtok
    ;stergem de pe stiva ce am pushat
    add esp, 8

repeta:
    ;comparam eax cu 0
    cmp eax, 0
    je end
    ;ii atribuim lui ecx valoarea de la adresa [ebp-4]
    mov ecx, [ebp-4]
    ;comparam ecx cu ce se afla la adresa [ebp+16]
    cmp ecx, [ebp+16]
    jge end
    ;ii atribuim lui edx valoarea de la adresa [ebp+12]
    mov edx, [ebp+12]
    ;pentru inmultire
    mov [edx + ecx*4], eax
    ;incrementam ce se afla la adresa [ebp-4]
    inc dword [ebp-4]
    push delimitatori
    ;pentru a da push la 0 ( strtok(NULL, " "); )
    push 0
    call strtok
    ;pentru a sterge ce am pushat
    add esp, 8
    jmp repeta

end:
    leave
    ret

;; sort(char **words, int number_of_words, int size)
;  functia va trebui sa apeleze qsort pentru soratrea cuvintelor 
;  dupa lungime si apoi lexicografix

compare:
    ; create a new stack frame
    enter 0, 0
    push esi
    push edi
    push ebx
    ;pentru a atribui esi ce se afla la adresa [ebp+8]
    mov esi, [ebp+8]
    mov esi, [esi]
    ;pentru a atrbui lui edi ce se afla la adrea [ebp+12]
    mov edi, [ebp+12]
    mov edi, [edi]
    push esi
    call strlen
    ;pentru a sterge ce am pushat
    add esp, 4
    mov ebx, eax
    push edi
    call strlen
    ;pentru a sterge ce am pushat
    add esp, 4
    mov ecx, eax
    cmp ebx, ecx
    jne difera_lungime

    push edi
    push esi
    call strcmp
    ;pentru a sterge ce am pushat
    add esp, 8
    jmp sfarsit

difera_lungime:
    mov eax, ebx
    sub eax, ecx

sfarsit:
    pop ebx
    pop edi
    pop esi
    pop ebp
    ret

sort:
    ; create a new stack frame
    enter 0, 0
    pusha
    push compare
    ;pentru a pusha pe stiva
    push dword [ebp+16]
    ;pentru a pusha pe stiva
    push dword [ebp+12]
    ;pentru a pusha pe stiva
    push dword [ebp+8]
    call qsort
    ;pentru a sterge ce am pushat
    add esp, 16
    popa
    leave
    ret

