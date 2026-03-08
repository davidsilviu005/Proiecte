%include "../include/io.mac"

; declare your structs here

section .data

section .text
    global check_events
    extern printf

check_events:
    ;; DO NOT MODIFY
    enter 0,0
    pusha

    mov ebx, [ebp + 8]      ; events
    mov ecx, [ebp + 12]     ; length
    ;; DO NOT MODIFY

    ;; Your code starts here

    mov esi, ebx

repeta:
    ;esi+31 -> valid
    ;esi+32 -> day
    ;esi+33 -> month
    ;esi+34 -> year
    mov byte[esi+31], 0


    cmp word[esi+34], 1990
    jl invalid
    cmp word[esi+34], 2030
    jg invalid
    cmp byte[esi+33], 1
    jl invalid
    cmp byte[esi+33], 12
    jg invalid


    ;1,3,5,7,8,10,12 -> 31 zile
    ;4,6,9,11 -> 30 zile
    ;2 -> 28 zile

    cmp byte[esi+32], 1
    jl invalid



    cmp byte[esi+33], 1
    je azile
    cmp byte[esi+33], 3
    je azile
    cmp byte[esi+33], 5
    je azile
    cmp byte[esi+33], 7
    je azile
    cmp byte[esi+33], 8
    je azile
    cmp byte[esi+33], 10
    je azile
    cmp byte[esi+33], 12
    je azile

    cmp byte[esi+33], 4
    je bzile
    cmp byte[esi+33], 6
    je bzile
    cmp byte[esi+33], 9
    je bzile
    cmp byte[esi+33], 11
    je bzile

    cmp byte[esi+33], 2
    je czile
    

    azile:
        cmp byte[esi+32], 31
        jg invalid
        jmp gata
    bzile:
        cmp byte[esi+32], 30
        jg invalid
        jmp gata
    czile:
        cmp byte[esi+32], 28
        jg invalid
        jmp gata
    gata:
        mov byte[esi+31], 1
    invalid:
    add esi, 36
    dec ecx
    cmp ecx, 0
    jne repeta
    ;; Your code ends here

    ;; DO NOT MODIFY
    popa
    leave
    ret
    ;; DO NOT MODIFY