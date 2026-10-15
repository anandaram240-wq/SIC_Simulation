COUNT   START   9000
        LDX     ZERO
        LDA     ZERO
        STA     COUNT1
LOOP    LDA     TABLE
        COMP    ZERO
        JLT     NEXT
        LDA     COUNT1
        ADD     ONE
        STA     COUNT1
NEXT    TIX     FIVE
        JLT     LOOP
        RSUB
TABLE   WORD    10
        WORD    -5
        WORD    20
        WORD    -2
        WORD    15
COUNT1  RESW    1
ZERO    WORD    0
ONE     WORD    1
FIVE    WORD    5
        END     COUNT
