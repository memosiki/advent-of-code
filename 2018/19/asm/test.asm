
extern printf, exit
section .rodata
    message db "Register value %#d", 10, 0
section .data
    instructions dq seti_123_0_4_3607, bani_4_456_4_e805, eqri_4_72_4_55fc, addr_4_1_1_822b, seti_0_0_1_f9b7, seti_0_0_4_e9d2, bori_4_65536_5_0ed0, seti_10704114_0_4_e227, bani_5_255_2_9a18, addr_4_2_4_3190, bani_4_16777215_4_4660, muli_4_65899_4_34a8, bani_4_16777215_4_7200, gtir_256_5_2_3c1e, addr_2_1_1_fb18, addi_1_1_1_c1ac, seti_27_2_1_ce82, seti_0_4_2_832a, addi_2_1_3_62d1, muli_3_256_3_0537, gtrr_3_5_3_e529, addr_3_1_1_0082, addi_1_1_1_653f, seti_25_5_1_07d4, addi_2_1_2_a317, seti_17_5_1_6576, setr_2_6_5_2a10, seti_7_8_1_5a81, eqrr_4_0_2_8bec, addr_2_1_1_4570, seti_5_3_1_58b6
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
    cmp r11, r8
    jge answer

    mov rax, 8
    mul r11

    jmp [abs instructions + rax]

after_loop:
    inc r11
    jmp before_loop


seti_123_0_4_3607: ;seti 123 0 4

    mov r14, 123
    jmp after_loop

bani_4_456_4_e805: ;bani 4 456 4

    mov r14, 456
    and r14, r14
    jmp after_loop

eqri_4_72_4_55fc: ;eqri 4 72 4

    cmp r14, 72
    je eqri_4_72_4_55fc_eq
    xor r14, r14
    jmp after_loop
    eqri_4_72_4_55fc_eq: mov r14, 1
    jmp after_loop

addr_4_1_1_822b: ;addr 4 1 1

    mov r11, r14
    add r11, r11
    jmp after_loop

seti_0_0_1_f9b7: ;seti 0 0 1

    mov r11, 0
    jmp after_loop

seti_0_0_4_e9d2: ;seti 0 0 4

    mov r14, 0
    jmp after_loop

bori_4_65536_5_0ed0: ;bori 4 65536 5

    mov r15, 65536
    or r15, r14
    jmp after_loop

seti_10704114_0_4_e227: ;seti 10704114 0 4

    mov r14, 10704114
    jmp after_loop

bani_5_255_2_9a18: ;bani 5 255 2

    mov r12, 255
    and r12, r15
    jmp after_loop

addr_4_2_4_3190: ;addr 4 2 4

    mov r14, r14
    add r14, r12
    jmp after_loop

bani_4_16777215_4_4660: ;bani 4 16777215 4

    mov r14, 16777215
    and r14, r14
    jmp after_loop

muli_4_65899_4_34a8: ;muli 4 65899 4

    mov rax, 65899
    mul r14
    mov r14, rax
    jmp after_loop

bani_4_16777215_4_7200: ;bani 4 16777215 4

    mov r14, 16777215
    and r14, r14
    jmp after_loop

gtir_256_5_2_3c1e: ;gtir 256 5 2

    mov rax, 256cmp r15, rax
    jle gtir_256_5_2_3c1e_gr
    xor r12, r12
    jmp after_loop
    gtir_256_5_2_3c1e_gr: mov r12, 1
    jmp after_loop

addr_2_1_1_fb18: ;addr 2 1 1

    mov r11, r12
    add r11, r11
    jmp after_loop

addi_1_1_1_c1ac: ;addi 1 1 1

    mov r11, r11
    add r11, 1
    jmp after_loop

seti_27_2_1_ce82: ;seti 27 2 1

    mov r11, 27
    jmp after_loop

seti_0_4_2_832a: ;seti 0 4 2

    mov r12, 0
    jmp after_loop

addi_2_1_3_62d1: ;addi 2 1 3

    mov r13, r12
    add r13, 1
    jmp after_loop

muli_3_256_3_0537: ;muli 3 256 3

    mov rax, 256
    mul r13
    mov r13, rax
    jmp after_loop

gtrr_3_5_3_e529: ;gtrr 3 5 3

    cmp r15, r13
    jb gtrr_3_5_3_e529_gr
    xor r13, r13
    jmp after_loop
    gtrr_3_5_3_e529_gr: mov r13, 1
    jmp after_loop

addr_3_1_1_0082: ;addr 3 1 1

    mov r11, r13
    add r11, r11
    jmp after_loop

addi_1_1_1_653f: ;addi 1 1 1

    mov r11, r11
    add r11, 1
    jmp after_loop

seti_25_5_1_07d4: ;seti 25 5 1

    mov r11, 25
    jmp after_loop

addi_2_1_2_a317: ;addi 2 1 2

    mov r12, r12
    add r12, 1
    jmp after_loop

seti_17_5_1_6576: ;seti 17 5 1

    mov r11, 17
    jmp after_loop

setr_2_6_5_2a10: ;setr 2 6 5

    mov r15, r12
    jmp after_loop

seti_7_8_1_5a81: ;seti 7 8 1

    mov r11, 7
    jmp after_loop

eqrr_4_0_2_8bec: ;eqrr 4 0 2

    cmp r14, r10
    je eqrr_4_0_2_8bec_eq
    xor r12, r12
    jmp after_loop
    eqrr_4_0_2_8bec_eq: mov r12, 1
    jmp after_loop

addr_2_1_1_4570: ;addr 2 1 1

    mov r11, r12
    add r11, r11
    jmp after_loop

seti_5_3_1_58b6: ;seti 5 3 1

    mov r11, 5
    jmp after_loop


answer:
    sub   rsp, 8
    ; Call printf.
    mov   rsi, r11
    lea   rdi, [rel message]
    xor   eax, eax
    call  printf

    ; Return from main.
    xor   eax, eax
    add   rsp, 8
    ret