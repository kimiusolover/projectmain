.set noreorder
.text
.globl _start
.ent _start

_start:
    andi  $t0, $sp, 7
    bnez  $t0, bad_stack
    nop

    addiu $sp, $sp, -16
    jal   AbiRunChecks
    nop
    addiu $sp, $sp, 16

    move  $a0, $v0
    b     finish
    nop

bad_stack:
    li    $a0, 5

finish:
    li    $v0, 4001
    syscall
    break

.end _start
