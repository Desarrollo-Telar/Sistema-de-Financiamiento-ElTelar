// Programa en ensamblador para generar números naturales en un archivo de texto

section .data
    filename db "numeros.txt", 0    // Nombre del archivo
    msg db "números naturales generados", 0

section .bss
    buffer resb 1024                // Buffer para los números

section .text
    global _start

_start:
    // Abrir archivo
    mov eax, 8                      // sys_open
    mov ebx, filename
    mov ecx, 2                      // O_WRONLY
    int 0x80

    // Guardar descriptor de archivo
    mov ebx, eax

    // Generar números y escribir en el archivo
    mov ecx, 1                      // Contador de números
    mov edx, buffer

generate_numbers:
    // Convertir número a cadena
    mov eax, ecx
    call int_to_str

    // Añadir cero y nueva línea
    mov byte [edx], 0
    inc edx
    mov byte [edx], 10
    inc edx


    inc ecx


    cmp ecx, 10                     
    jle generate_numbers

    // Escribir buffer en el archivo
    mov eax, 4                      
    mov ecx, buffer
    mov edx, edx
    int 0x80

    // Cerrar archivo
    mov eax, 6                      
    int 0x80

    // Salida
    mov eax, 1                      // sys_exit
    int 0x80

// Rutina para convertir entero a cadena
int_to_str:
    push eax
    mov ebx, 10
    xor ecx, ecx

convert_loop:
    xor edx, edx
    div ebx
    add dl, '0'
    push edx
    inc ecx
    test eax, eax
    jnz convert_loop

print_loop:
    pop eax
    mov [edx], al
    inc edx
    loop print_loop

    pop eax
    ret
