%include "../include/io.mac"

extern printf
global base64

section .data
	alphabet db 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/'
	fmt db "%d", 10, 0

section .text

base64:
    ;; DO NOT MODIFY

    push ebp
    mov ebp, esp
    pusha

    mov esi, [ebp + 8] ; source array
    mov ebx, [ebp + 12] ; n
    mov edi, [ebp + 16] ; dest array
    mov edx, [ebp + 20] ; pointer to dest length

    ;; DO NOT MODIFY


    ; -- Your code starts here --

    mov ecx, ebx
    mov dword[edx], 0

    repeat:
        ; char 1
        mov eax, 0
        mov al, [esi]
        and al, 11111100b
        shr al, 2

        mov al, [alphabet + eax]
        mov [edi], al
        inc edi

        ; char 2
        mov al, [esi+1]
        shr al, 4
        mov bl, [esi]
        and bl, 11b
        shl bl, 4
        add al, bl

        mov al, [alphabet + eax]
        mov [edi], al
        inc edi

        ; char 3
        mov al, [esi+1]
        and al, 1111b
        shl al, 2
        mov bl, [esi+2]
        shr bl, 6
        add al, bl

        mov al, [alphabet + eax]
        mov [edi], al
        inc edi

        ; char 4
        mov al, [esi+2]
        and al, 111111b

        mov al, [alphabet + eax]
        mov [edi], al
        inc edi

        add esi, 3
        add dword[edx], 4
        sub ecx, 3
        cmp ecx, 0
        jg repeat

    ; -- Your code ends here --


    ;; DO NOT MODIFY

    popa
    leave
    ret

    ;; DO NOT MODIFY