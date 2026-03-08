section .data
    ;pentru a declara variabila string_gol
    string_gol db "", 0

section .text
global check_palindrome
global composite_palindrome
extern strcmp
extern strlen
extern free
extern strcpy
extern strdup

check_palindrome:
    ; create a new stack frame
    enter 0, 0
    push esi
    push edi
    push ebx
    ;pentru a atrbui lui esi ce se afla la adresa [ebp+8]
    mov esi, [ebp+8]
    xor edi, edi

lungime:
    ;pentru a compara byte[esi+edi] cu 0
    cmp byte[esi+edi], 0
    je sfarsit_lungime
    inc edi
    jmp lungime

sfarsit_lungime:
    test edi, edi
    jz e_palindrom
    ;pentru a compara edi cu 1
    cmp edi, 1
    je e_palindrom
    xor edx, edx
    ;pentrua lua adresa [edi-1]
    lea ecx, [edi-1]

repeta:
    cmp edx, ecx
    jge e_palindrom
    mov al, [esi+edx]
    mov bl, [esi+ecx]
    cmp al, bl
    jne nu_e_palindrom
    inc edx
    dec ecx
    jmp repeta

e_palindrom:
    ;pentru a atribui lui eax valoarea 1
    mov eax, 1
    jmp return

nu_e_palindrom:
    xor eax, eax

return:
    pop ebx
    pop edi
    pop esi
    leave
    ret

composite_palindrome:
    ; create a new stack frame
    enter 0, 0
    ;pentru a scadea de la esp 164
    sub esp, 164
    ;pentru a lua adresa [ebp-160]
    lea edi, [ebp-160]
    ;ecx primeste valoarea 40
    mov ecx, 40
    xor eax, eax

curata_buffer:
    mov [edi], eax
    ;pentru a incrementa edi cu 4
    add edi, 4
    dec ecx
    jnz curata_buffer
    ;facem ce e la dword [ebp-164] 0
    mov dword [ebp-164], 0
    ;pentru a lua adresa [ebp-164]
    lea eax, [ebp-164]
    push eax
    ;pentru a pusha 0
    push 0
    ;pentru a lua adresa [ebp-160]
    lea eax, [ebp-160]
    push eax
    ;pentru a pusha dword [ebp+12]
    push dword [ebp+12]
    ;pentru a pusha [ebp+8]
    push dword [ebp+8]
    ;pentru a pusha 0
    push 0
    call generare
    ;pentru a sterge ce am pushat
    add esp, 24
    ;pentru a atribui lui eax ce se afla la adresa [ebp-164]
    mov eax, [ebp-164]
    test eax, eax
    jnz return_var_buna
    push string_gol
    call strdup
    ;pentru a sterge ce am pushat
    add esp, 4
    jmp ceva

return_var_buna:
    ;pentru a atribui lui eax ce se afla la adresa [ebp-164]
    mov eax, [ebp-164]

ceva:
    mov esp, ebp
    pop ebp
    ret

generare:
    push ebp
    mov ebp, esp
    push ebx
    push esi
    push edi
    ;pentru a atribui lui eax ce se afla la adresa [ebp+8]
    mov eax, [ebp+8]
    ;pentru a compara eax cu ce se afla la adresa [ebp+16] 
    cmp eax, [ebp+16]
    jne recursiv
    ;pentru a atribui lui eax ce se afla la adresa [ebp+20]
    mov eax, [ebp+20]
    ;pentru a adauga lui eax ce se afla la adrea [ebp+24]
    add eax, [ebp+24]
    ;pentru a atribui byte [eax] 0
    mov byte [eax], 0
    ;pentru a pusha
    push dword [ebp+20]
    call check_palindrome
    ;pentru a sterge ce am pushat
    add esp, 4
    test eax, eax
    jz sf_generare
    ;pentru a atribui lui edi ce se afla la adresa [ebp+28]
    mov edi, [ebp+28]
    mov ebx, [edi]
    ;pentrur a pusha
    push dword [ebp+20]
    call strlen
    ;pentru a sterge ce am pushat
    add esp, 4
    mov esi, eax
    test ebx, ebx
    jz schimba
    push ebx
    call strlen
    ;pentru a sterge ce am pushat
    add esp, 4
    cmp esi, eax
    jg schimba
    jl sf_generare
    push ebx
    ;pentru a pusha
    push dword [ebp+20]
    call strcmp
    ;pentru a sterge ce am pushat
    add esp, 8
    test eax, eax
    jge sf_generare

schimba:
    push dword [edi]
    call free
    ;pentru a sterge ce am pushat
    add esp, 4
    ;pentru a pusha
    push dword [ebp+20]
    call strdup
    ;pentru a sterge ce am pushat
    add esp, 4
    mov [edi], eax
    jmp sf_generare

recursiv:
    ;pentru a pusha
    push dword [ebp+28]
    ;pentru a pusha
    push dword [ebp+24]
    ;pentru a pusha
    push dword [ebp+20]
    ;pentru a pusha
    push dword [ebp+16]
    ;pentru a pusha
    push dword [ebp+12]
    ;pentru a atribui lui eax ce se afla la adresa [ebp+8]
    mov eax, [ebp+8]
    inc eax
    push eax
    call generare
    ;pentru a sterge ce am pushat
    add esp, 24

    ;pentru a atribui lui eax ce se afla la adresa [ebp+12]
    mov eax, [ebp+12]
    ;pentru a atribui lui edx ce se afla la adresa [ebp+8]
    mov edx, [ebp+8]
    ;pentru inmultire
    mov ebx, [eax+edx*4]
    push ebx
    call strlen
    ;pentru a sterge ce am pushat
    add esp, 4
    mov edi, eax

    ;pentru a atribui lui eax ce se afla la adresa [ebp+20]
    mov eax, [ebp+20]
    ;pebtru a adauga lui eax ce se afla la adresa [ebp+24]
    add eax, [ebp+24]
    push ebx
    push eax
    call strcpy
    ;pentru a sterge ce am pushat
    add esp, 8

    ;pentru a atribui lui esi ce se afla la adresa [ebp+24]
    mov esi, [ebp+24]
    add esi, edi
    ;pentru a pusha
    push dword [ebp+28]
    push esi

    ;pentru a pusha
    push dword [ebp+20]
    ;pentru a pusha
    push dword [ebp+16]
    ;pentru a pusha
    push dword [ebp+12]
    ;pentru a atrbui lui eax ce se afla la adrea [ebp+8]
    mov eax, [ebp+8]
    inc eax
    push eax
    call generare
    ;pentru a sterge ce am pushat
    add esp, 24

sf_generare:
    pop edi
    pop esi
    pop ebx
    pop ebp
    ret



