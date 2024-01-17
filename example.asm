global _start

section .text
_start:
    mov eax, 1 ; moves 1 to a general purpose register called eax
    mov ebx, 42 ; similar
    sub ebx, 29 ; ebx -= 29
    add ebx, ecx ; ebx += ecx
    mul ebx ; eax *= ebx
    div edx ; eax /= edx
    int 0x82 ; this performs an interrupt, this means that the processor will transfer control to an interrupt handler that we've specified by the following value
    ; in this case we are using the hex value, which is the interrupt handler for system calls.
    ; The system calls it makes is determined by the eax register. The value 1 means that we are making a system exit call.
    ; The value in ebx will be exit status for our program.

example 2

global _start

section .data
    msg db "Hello, world!", 0x0a
    len equ $ - msg

section .text
_start:
    mov eax, 4    ; sys_write system call
    mov ebx, 1    ; stdout file descriptor
    mov ecx, msg  ; bytes to write
    mov edx, len  ; number of bytes to write
    int 0x80      ; perform system call
    mov eax, 1    ; sys_exit system call
    mov ebx, 0    ; exit status is 0
    int 0x80

example 3

global _start

section .text
_start:
   mov ebx, 42   ; exit status is 42
   mov eax, 1    ; sys_exit system call
   jmp skip       ; jump to skip
   mov ebx, 13   ; exit status is 13, but is not executed since its never executed
skip:
   int 0x80

example 4

global _start

section .text
_start:
   mov ecx, 99   ; set ecx to 99
   mov ebx, 42   ; exit status is 42
   mov eax, 1    ; sys_exit system call
   cmp ecx, 100  ; compare ecx to 100
   jl skip       ; jump if less than
   mov ebx, 13   ; exit status is 13
skip:
   int 0x80

simple loop

global _start

section .text
_start:
    mov ebx, 1    ; start ebx at 1
    mov ecx, 6    ; number of iterations
label:
    add ebx, ebx  ; ebx += ebx
    dec ecx       ; ecx -= 1
    cmp ecx, 0    ; compare ecx with 0
    jg label      ; jump to label if greater
    mov eax, 1    ; sys_exit system call
    int 0x80