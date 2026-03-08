%include "../include/io.mac"

extern printf
global check_row
global check_column
global check_box

section .data
    buffer dd 0
    buffer0 resb 9
    ; pentru cifrele 1-9 (index 0 = cifra 1)

section .text

; int check_row(char* sudoku, int row);
check_row:
    ;; DO NOT MODIFY
    push    ebp
    mov     ebp, esp
    push ebx
    push ecx
    push edx
    push esi
    push edi

    mov     esi, [ebp + 8]  ; char* sudoku
    mov     edx, [ebp + 12]  ; int row
    ;; DO NOT MODIFY

    ;; Freestyle starts here
    mov ecx, 9
    mov edi, buffer0
rand:
    mov byte [edi], 0
    inc edi
    loop rand

    mov ecx, 0
urmatoarea_coloana:
    ; rand * 9
    mov eax, edx
    imul eax, 9
    ; index = rand * 9 + coloana
    add eax, ecx
    mov bl, [esi + eax]

    cmp bl, 1
    jb rand_invalid
    cmp bl, 9
    ja rand_invalid

    mov [buffer], bl
    mov ebx, 0
    mov bl, [buffer]   

    ; ajustare index (cifra - 1)
    dec ebx               
    mov al, [buffer0 + ebx]
    cmp al, 0
    jne rand_invalid
    mov byte [buffer0 + ebx], 1

    inc ecx
    cmp ecx, 9
    jl urmatoarea_coloana

    mov eax, 1
    jmp end_check_row
rand_invalid:
    mov eax, 2
    ;; Freestyle ends here
end_check_row:
    ;; DO NOT MODIFY
    pop edi
    pop esi
    pop edx
    pop ecx
    pop ebx
    leave
    ret

; int check_column(char* sudoku, int column);
check_column:
    ;; DO NOT MODIFY
    push    ebp
    mov     ebp, esp
    push ebx
    push ecx
    push edx
    push esi
    push edi

    mov     esi, [ebp + 8]  ; char* sudoku
    mov     edx, [ebp + 12]  ; int column
    ;; DO NOT MODIFY

    ;; Freestyle starts here
    mov ecx, 9
    mov edi, buffer0
coloana:
    mov byte [edi], 0
    inc edi
    loop coloana

    mov ecx, 0
urmatorul_rand:
    mov eax, ecx
    imul eax, 9
    ; index = rand * 9 + coloana
    add eax, edx           
    mov bl, [esi + eax]

    cmp bl, 1
    jb coloana_invalida
    cmp bl, 9
    ja coloana_invalida

    mov [buffer], bl
    mov ebx, 0
    mov bl, [buffer]  

    dec ebx
    mov al, [buffer0 + ebx]
    cmp al, 0
    jne coloana_invalida
    mov byte [buffer0 + ebx], 1

    inc ecx
    cmp ecx, 9
    jl urmatorul_rand

    mov eax, 1
    jmp end_check_column
coloana_invalida:
    mov eax, 2
    ;; Freestyle ends here
end_check_column:
    ;; DO NOT MODIFY
    pop edi
    pop esi
    pop edx
    pop ecx
    pop ebx
    leave
    ret

; int check_box(char* sudoku, int box);
check_box:
    ;; DO NOT MODIFY
    push    ebp
    mov     ebp, esp
    push ebx
    push ecx
    push edx
    push esi
    push edi

    mov     esi, [ebp + 8]  ; char* sudoku
    mov     edx, [ebp + 12]  ; int box
    ;; DO NOT MODIFY

    ;; Freestyle starts here
    mov ecx, 9
    mov edi, buffer0
box:
    mov byte [edi], 0
    inc edi
    loop box

    mov eax, edx
    xor edx, edx
    mov ebx, 3
    div ebx
    mov edi, eax
    mov ebx, edx
    imul edi, 27
    imul ebx, 3
    add edi, ebx
    mov ecx, 0

urm_box:
    mov eax, ecx
    mov edx, 0
    mov ebx, 3
    div ebx
    imul eax, 9
    add eax, edx
    add eax, edi

    mov bl, [esi + eax]
    cmp bl, 1
    jb invalid_box
    cmp bl, 9
    ja invalid_box

    mov [buffer], bl
    mov ebx, 0
    mov bl, [buffer]  
    
    dec ebx
    mov al, [buffer0 + ebx]
    cmp al, 0
    jne invalid_box
    mov byte [buffer0 + ebx], 1

    inc ecx
    cmp ecx, 9
    jl urm_box

    mov eax, 1
    jmp end_check_box
invalid_box:
    mov eax, 2
    ;; Freestyle ends here
end_check_box:
    ;; DO NOT MODIFY
    pop edi
    pop esi
    pop edx
    pop ecx
    pop ebx
    leave
    ret