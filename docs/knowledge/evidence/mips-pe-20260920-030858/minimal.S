.set noreorder
.set nomips16
.text
.globl MinimalEntry
.ent MinimalEntry
MinimalEntry:
    move $v0, $zero
    jr   $ra
    nop
.end MinimalEntry
