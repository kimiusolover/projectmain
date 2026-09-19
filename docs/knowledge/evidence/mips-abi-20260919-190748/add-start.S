.set noreorder
.text
.globl _start
.ent _start

_start:
    # 呼出前のスタック整列を確認
    andi  $t0, $sp, 7
    bnez  $t0, fail
    nop

    # o32 の引数領域を確保
    addiu $sp, $sp, -16

    # ProbeAdd(10, 7)
    li    $a0, 10
    jal   ProbeAdd
    li    $a1, 7

    addiu $sp, $sp, 16

    # 戻り値が17なら成功
    li    $t0, 17
    bne   $v0, $t0, fail
    nop

    move  $a0, $zero
    b     finish
    nop

fail:
    li    $a0, 1

finish:
    # Linux MIPS o32 の exit(status)
    li    $v0, 4001
    syscall
    break

.end _start
