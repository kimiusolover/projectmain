.set noreorder
.set nomips16

.section .text,"ax",@progbits
.balign 16
.globl MinimalEntry
.type MinimalEntry, @function
MinimalEntry:
    move $v0, $zero
    jr   $ra
    nop
.size MinimalEntry, .-MinimalEntry

.section .data,"aw",@progbits
.balign 4

.globl ProbeValue
.type ProbeValue, @object
ProbeValue:
    .word 0x12345678
.size ProbeValue, 4

.globl ProbePointer
.type ProbePointer, @object
ProbePointer:
    .word ProbeValue
.size ProbePointer, 4
