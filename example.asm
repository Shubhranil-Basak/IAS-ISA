global _start

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