.target "appleii"
printc = $FDF0

.org $801
; Prints all characters

    LDA #0
main_loop:
    ; X = A; X++; A = X
    TAX
    INX
    TXA
    ; Wait for a lil bit
    LDY #0
inner_loop:
    INY
    BNE inner_loop
    JSR printc
    JMP main_loop
