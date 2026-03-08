section .data
    ;pentru a initializa valoarea cu 0
    min_anterior dd 0
    ;pentru a initializa valoarea cu 0
    min_nou dd 0
    ;pentru a initializa valoarea cu 0
    primul_gasit db 0
    ;pentru a initializa valoarea cu 0
    varf dd 0

section .text
global sort

;   struct node {
;    int val;
;    struct node* next;
;   };

;; struct node* sort(int n, struct node* node);
;   The function will link the nodes in the array
;   in ascending order and will return the address
;   of the new found head of the list
; @params:
;   n -> the number of nodes in the array
;   node -> a pointer to the beginning in the array
;   @returns:
;   the address of the head of the sorted list
sort:
    ; create a new stack frame
    enter 0, 0
    xor eax, eax
    ;pentru accesarea stivei la esp+8
    mov ecx, [esp+8]
    ;pentru accesarea stivei la esp+12
    mov esi, [esp+12]
    mov edi, esi

prima_cautare:
    mov eax, [edi]
    ;verificare daca eax e 1
    cmp eax, 1
    je gasit_min
    ;adaugam lui edi 8
    add edi, 8
    loop prima_cautare

gasit_min:
    mov [min_anterior], edi
    mov [varf], edi
    ;eax primeste valoarea [esp+8]
    mov ecx, [esp+8]
    dec ecx

repeta:
    ;facem byte[primul_gasit] 0
    mov byte[primul_gasit], 0
    ;edx primeste valoarea [esp+8]
    mov edx, [esp+8]
    ;esi primeste valoarea [esp+12]
    mov esi, [esp+12]

repeta2:
    ;comparam byte[primul_gasit] cu 0
    cmp byte[primul_gasit], 0
    jne nu_e_primul
    mov eax, [min_anterior]
    mov ebx, [eax]
    cmp [esi], ebx
    jle skip
    mov [min_nou], esi
    ;facem byte[primul_gasit] 1
    mov byte[primul_gasit], 1
    jmp skip

nu_e_primul:
    mov eax, [min_nou]
    mov eax, [eax]
    cmp [esi], ebx
    jle skip
    cmp [esi], eax
    jge skip
    mov [min_nou], esi

skip:
    ;esi + 8
    add esi, 8
    dec edx
    ;compara edx cu 00
    cmp edx, 0
    jne repeta2
    mov eax, [min_anterior]
    mov ebx, [min_nou]
    ;accesam [eax+4]
    mov [eax+4], ebx
    mov eax, [min_nou]
    mov [min_anterior], eax
    dec ecx
    ;comparam ecx cu 0
    cmp ecx, 0
    jne repeta
    mov eax, [varf]
    leave
    ret

