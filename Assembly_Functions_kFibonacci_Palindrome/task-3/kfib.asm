section .text
global kfib

kfib:
    ; create a new stack frame
    enter 0, 0
    xor eax, eax
    push esi
    push edi
    push ebx
    ;eax primeste ce se afla la adresa [ebp+8]
    mov eax, [ebp+8]
    ;ecx primeste ce se afla la adresa [ebp+12]
    mov ecx, [ebp+12]
    cmp eax, ecx
    jl zero
    cmp eax, ecx
    je unu
    ;esi primeste val 0
    mov esi, 0
    ;edi primeste valoarea 1
    mov edi, 1

repeta:
    cmp edi, ecx
    jg sfarsit
    push ecx
    push eax
    mov ebx, eax
    sub ebx, edi
    push ecx
    push ebx
    call kfib
    ;pentru a sterge ce am pushat
    add esp, 8
    add esi, eax
    pop eax
    pop ecx
    inc edi
    jmp repeta

sfarsit:
    mov eax, esi
    jmp end

zero:
    ;pentru a atribui lui eax valoarea 0
    mov eax, 0
    jmp end

unu:
    ;pentru a atribui lui eax valoarea 1
    mov eax, 1

end:
    pop ebx
    pop edi
    pop esi
    pop ebp
    ret

