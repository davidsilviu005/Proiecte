%include "../include/io.mac"

; declare your structs here

section .data
    i dd 0
    j dd 0

section .text
    global sort_events
    extern printf
    extern strcmp

compare:
    pusha
    ; verificam daca e valid
    mov al, [esi+31]
    mov bl, [edi+31]
    cmp al, bl
    ja compare_false
    jb compare_true
    
    ; verificam care este prima cronologic
    mov ax, [esi+34]
    mov bx, [edi+34]
    cmp ax, bx
    ja compare_true
    jb compare_false
    
    mov al, [esi+33]
    mov bl, [edi+33]
    cmp al, bl
    ja compare_true
    jb compare_false
    
    mov al, [esi+32]
    mov bl, [edi+32]
    cmp al, bl
    ja compare_true
    jb compare_false

    ; verificam numele -> strcmp(v[i].name, v[j].name)
    push edi
    push esi
    call strcmp
    add esp, 2*4
    
    cmp eax, 0
    jl compare_false
    
    compare_true:
        popa
        mov eax, 1
        jmp compare_over
    
    compare_false:
        popa
        mov eax, 0
        
    compare_over:
        ret
    
swap:
    ; swap(v[i], v[j]), struct size 36 biti
    pusha
    mov ebx, 36

    swap_repeat:
        ; al <- [esi]
        ; [esi] <- [edi]
        ; [edi] <- al
        
        mov al, [esi]
        
        mov dl, [edi]
        mov [esi], dl
        
        mov [edi], al
        
        inc esi
        inc edi
        dec ebx
        cmp ebx, 0
        ja swap_repeat
        
    popa
    ret
    
sort_events:
    ;; DO NOT MODIFY
    enter 0, 0
    pusha

    mov ebx, [ebp + 8]      ; events
    mov ecx, [ebp + 12]     ; length
    ;; DO NOT MODIFY

    ;; Your code starts here

    ;esi -> name (char*)
    ;esi+31 -> valid (byte)
    ;esi+32 -> day (byte)
    ;esi+33 -> month (byte)
    ;esi+34 -> year (word)

    ; i -> 1, n-1
    ; j -> i+1, n 
        
    ; esi -> v[i]
    ; edi -> v[j]
    
    mov esi, ebx
    ; i = 1
    mov dword[i], 1
    
repeta1:
    mov edi, esi
    add edi, 36
    ; j = i+1
    mov eax, [i]
    mov [j], eax
    inc dword[j]

    repeta2:
        call compare
        cmp eax, 1
        jne no_swap

        call swap

        no_swap:
        add edi, 36
        ; ++j
        inc dword[j]
        cmp dword[j], ecx
        jle repeta2
    
    add esi, 36
    ; ++i
    inc dword[i]
    cmp dword[i], ecx
    jl repeta1



    ;; Your code ends here

    ;; DO NOT MODIFY
    popa
    leave
    ret
    ;; DO NOT MODIFY
    
