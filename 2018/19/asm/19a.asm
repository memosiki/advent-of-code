
extern printf, exit
section .rodata
    message db "Register value %#d", 10, 0
section .data
    instructions dq addi_4_16_4_8faf, seti_1_4_3_6054, seti_1_3_5_6450, mulr_3_5_1_3674, eqrr_1_2_1_0613, addr_1_4_4_6255, addi_4_1_4_f839, addr_3_0_0_f2ce, addi_5_1_5_eb05, gtrr_5_2_1_43c1, addr_4_1_4_7bd0, seti_2_9_4_437a, addi_3_1_3_f5fc, gtrr_3_2_1_2b06, addr_1_4_4_e005, seti_1_6_4_ee7b, mulr_4_4_4_c37b, addi_2_2_2_882f, mulr_2_2_2_f183, mulr_4_2_2_8367, muli_2_11_2_518c, addi_1_2_1_a93a, mulr_1_4_1_96be, addi_1_7_1_f75f, addr_2_1_2_0965, addr_4_0_4_f2f4, seti_0_8_4_2a2d, setr_4_3_1_d167, mulr_1_4_1_4351, addr_4_1_1_7956, mulr_4_1_1_455c, muli_1_14_1_213c, mulr_1_4_1_ee74, addr_2_1_2_c599, seti_0_3_0_d14e, seti_0_6_4_2830
    instructions_count equ ($ - instructions) / 8
section .text

global main
main:
    ; elven asm instruction pointer
    xor rdi, rdi
    ; registers = r10 r11 r12 r13 r14 r15
    xor r10, r10
    xor r11, r11
    xor r12, r12
    xor r13, r13
    xor r14, r14
    xor r15, r15
    mov r8, instructions_count

before_loop:
    cmp r14, r8
    jge answer

    mov rax, 8
    mul r14

    jmp [abs instructions + rax]

after_loop:
    inc r14
    jmp before_loop


addi_4_16_4_8faf: ;addi 4 16 4

    mov r14, r14
    add r14, 16
    jmp after_loop

seti_1_4_3_6054: ;seti 1 4 3

    mov r13, 1
    jmp after_loop

seti_1_3_5_6450: ;seti 1 3 5

    mov r15, 1
    jmp after_loop

mulr_3_5_1_3674: ;mulr 3 5 1

    mov rax, r13
    mul r15
    mov r11, rax
    jmp after_loop

eqrr_1_2_1_0613: ;eqrr 1 2 1

    cmp r11, r12
    je eqrr_1_2_1_0613_eq
    xor r11, r11
    jmp after_loop
    eqrr_1_2_1_0613_eq: mov r11, 1
    jmp after_loop

addr_1_4_4_6255: ;addr 1 4 4

    mov r14, r11
    add r14, r14
    jmp after_loop

addi_4_1_4_f839: ;addi 4 1 4

    mov r14, r14
    add r14, 1
    jmp after_loop

addr_3_0_0_f2ce: ;addr 3 0 0

    mov r10, r13
    add r10, r10
    jmp after_loop

addi_5_1_5_eb05: ;addi 5 1 5

    mov r15, r15
    add r15, 1
    jmp after_loop

gtrr_5_2_1_43c1: ;gtrr 5 2 1

    cmp r15, r12
    jg gtrr_5_2_1_43c1_gr
    xor r11, r11
    jmp after_loop
    gtrr_5_2_1_43c1_gr: mov r11, 1
    jmp after_loop

addr_4_1_4_7bd0: ;addr 4 1 4

    mov r14, r14
    add r14, r11
    jmp after_loop

seti_2_9_4_437a: ;seti 2 9 4

    mov r14, 2
    jmp after_loop

addi_3_1_3_f5fc: ;addi 3 1 3

    mov r13, r13
    add r13, 1
    jmp after_loop

gtrr_3_2_1_2b06: ;gtrr 3 2 1

    cmp r13, r12
    jg gtrr_3_2_1_2b06_gr
    xor r11, r11
    jmp after_loop
    gtrr_3_2_1_2b06_gr: mov r11, 1
    jmp after_loop

addr_1_4_4_e005: ;addr 1 4 4

    mov r14, r11
    add r14, r14
    jmp after_loop

seti_1_6_4_ee7b: ;seti 1 6 4

    mov r14, 1
    jmp after_loop

mulr_4_4_4_c37b: ;mulr 4 4 4

    mov rax, r14
    mul r14
    mov r14, rax
    jmp after_loop

addi_2_2_2_882f: ;addi 2 2 2

    mov r12, r12
    add r12, 2
    jmp after_loop

mulr_2_2_2_f183: ;mulr 2 2 2

    mov rax, r12
    mul r12
    mov r12, rax
    jmp after_loop

mulr_4_2_2_8367: ;mulr 4 2 2

    mov rax, r14
    mul r12
    mov r12, rax
    jmp after_loop

muli_2_11_2_518c: ;muli 2 11 2

    mov rax, 11
    mul r12
    mov r12, rax
    jmp after_loop

addi_1_2_1_a93a: ;addi 1 2 1

    mov r11, r11
    add r11, 2
    jmp after_loop

mulr_1_4_1_96be: ;mulr 1 4 1

    mov rax, r11
    mul r14
    mov r11, rax
    jmp after_loop

addi_1_7_1_f75f: ;addi 1 7 1

    mov r11, r11
    add r11, 7
    jmp after_loop

addr_2_1_2_0965: ;addr 2 1 2

    mov r12, r12
    add r12, r11
    jmp after_loop

addr_4_0_4_f2f4: ;addr 4 0 4

    mov r14, r14
    add r14, r10
    jmp after_loop

seti_0_8_4_2a2d: ;seti 0 8 4

    mov r14, 0
    jmp after_loop

setr_4_3_1_d167: ;setr 4 3 1

    mov r11, r14
    jmp after_loop

mulr_1_4_1_4351: ;mulr 1 4 1

    mov rax, r11
    mul r14
    mov r11, rax
    jmp after_loop

addr_4_1_1_7956: ;addr 4 1 1

    mov r11, r14
    add r11, r11
    jmp after_loop

mulr_4_1_1_455c: ;mulr 4 1 1

    mov rax, r14
    mul r11
    mov r11, rax
    jmp after_loop

muli_1_14_1_213c: ;muli 1 14 1

    mov rax, 14
    mul r11
    mov r11, rax
    jmp after_loop

mulr_1_4_1_ee74: ;mulr 1 4 1

    mov rax, r11
    mul r14
    mov r11, rax
    jmp after_loop

addr_2_1_2_c599: ;addr 2 1 2

    mov r12, r12
    add r12, r11
    jmp after_loop

seti_0_3_0_d14e: ;seti 0 3 0

    mov r10, 0
    jmp after_loop

seti_0_6_4_2830: ;seti 0 6 4

    mov r14, 0
    jmp after_loop


answer:
    sub   rsp, 8
    ; Call printf.
    mov   rsi, r14
    lea   rdi, [rel message]
    xor   eax, eax
    call  printf

    ; Return from main.
    xor   eax, eax
    add   rsp, 8
    ret