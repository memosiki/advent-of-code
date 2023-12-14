%macro seti 3
    mov %3, %1
    jmp after_loop
%endmacro

%macro setr 3
    mov %3, %1
    jmp after_loop
%endmacro

%macro addi 3
    mov r8, %1
    add r8, %2
    mov %3, r8
    jmp after_loop
%endmacro

%macro addr 3
    mov r8, %1
    mov r9, %2
    add r8, r9
    mov %3, r8
    jmp after_loop
%endmacro

%macro mulr 3
    mov r8, %1
    mov rax, %2
    mul r8
    mov %3, rax
    jmp after_loop
%endmacro

%macro muli 3
    mov r8, %1
    mov rax, %2
    mul r8
    mov %3, rax
    jmp after_loop
%endmacro

%macro eqrr 3
    cmp %1, %2
    je %%equalEqrr
    mov %3, 0

    jmp after_loop
%%equalEqrr:
    mov %3, 1
    jmp after_loop
%endmacro

%macro gtrr 3
    cmp %2, %1
    jb %%tGtrr
    mov %3, 0
    jmp after_loop

%%tGtrr:
    mov %3, 1
    jmp after_loop
%endmacro
