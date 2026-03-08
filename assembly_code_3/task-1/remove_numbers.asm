%include "../include/io.mac"

extern printf
global remove_numbers

section .data
    fmt db "%d", 10, 0

section .text

; function signature: 
; void remove_numbers(int *a, int n, int *target, int *ptr_len);

remove_numbers:
    ;; DO NOT MODIFY
    push    ebp
    mov     ebp, esp
    pusha

    mov     esi, [ebp + 8] ; source array
    mov     ebx, [ebp + 12] ; n
    mov     edi, [ebp + 16] ; dest array
    mov     edx, [ebp + 20] ; pointer to dest length

    ;; DO NOT MODIFY
    

    ;; Your code starts here

    xor ecx, ecx
    xor eax, eax
    mov ecx, ebx
    xor ebx, ebx
    
repeta:
    test dword[esi], 1
    jnz urmatorul
    xor eax, eax
    verif:
        inc eax
        rol dword[esi], 1
        cmp dword[esi], 1
        je urmatorul
        cmp eax, 32
        jl verif
    mov eax, dword[esi]
    mov dword[edi], eax
    add edi, 4
    inc ebx
    urmatorul:
    add esi, 4
    loop repeta
    
    mov dword[edx], ebx

    ;; Your code ends here
    

    ;; DO NOT MODIFY

    popa
    leave
    ret
    
    ;; DO NOT MODIFY