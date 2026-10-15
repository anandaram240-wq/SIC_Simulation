# Two-Pass SIC Assembler Simulator

**Course:** System Software and Compiler Design (23CS701) — Activity - I  
**Semester & Section:** VII Semester 'A' Section  
**Allotted Program:** `COUNT START 9000 ... END COUNT` (Positive/Negative Array Processing & Counting)  

---

## 📌 Project Overview

This project implements and simulates a **Two-Pass Assembler** for the **Simplified Instructional Computer (SIC)** architecture formulated by Leland L. Beck.

An assembler translates symbolic assembly code into machine-executable object code. A single-pass assembler cannot translate instructions that reference symbols declared later in the code (**Forward Reference Problem**). To resolve this, the assembler operates in two distinct passes:

1. **Pass 1 (Address Assignment & Symbol Definition):**
   * Initializes the Location Counter (`LOCCTR`) using the `START` address (`9000 H`).
   * Scans instructions, advances `LOCCTR` based on instruction length (Format 3 instructions = 3 bytes, `WORD` = 3 bytes, `RESW n` = $3 \times n$ bytes).
   * Populates the **Symbol Table (`SYMTAB`)** with label-to-address bindings.
   * Calculates total program length ($903F_{16} - 9000_{16} = 003F_{16} = 63 \text{ bytes}$).
   * Emits intermediate records for Pass 2.

2. **Pass 2 (Machine Code Translation & Record Construction):**
   * Translates mnemonics using the **Opcode Table (`OPTAB`)**.
   * Resolves target memory addresses from `SYMTAB`.
   * Evaluates constants, including **24-bit Two's Complement** arithmetic for negative integer values (`WORD -5` $\rightarrow$ `FFFFFB`, `WORD -2` $\rightarrow$ `FFFFFE`).
   * Assembles and formats the complete Object Program into standard **Header (`H`)**, **Text (`T`)**, and **End (`E`)** records.

---

## 📂 Project Structure & Deliverables

| File | Description |
| :--- | :--- |
| **`REPORT.md`** | **Comprehensive Academic Project Report** (Theory, Leland Beck SIC specs, Mermaid flowcharts, step-by-step trace, 2's complement analysis, conclusion). |
| **`PRESENTATION.md`** | **16-Slide Seminar Presentation Deck & Viva Guide** (Slide breakdown, speaker notes, comparison tables, top viva questions & answers). |
| **`index.html`** | **Interactive Web GUI Simulator** (Single-step Pass 1/Pass 2, visual SYMTAB, HTE record constructor, 2's complement math cards). |
| **`main.py`** | Terminal/CLI simulation driver (prints Pass 1, SYMTAB, Pass 2, and HTE records). |
| **`gui.py`** | Desktop Tkinter GUI simulator with visual step-by-step table highlighting. |
| **`pass1.py`** | Pass 1 engine: LOCCTR tracking, SYMTAB builder, intermediate file generator. |
| **`pass2.py`** | Pass 2 engine: Object code generator, 24-bit 2's complement handler, HTE constructor. |
| **`opcode_table.py`** | Operation Code dictionary (`OPTAB`) and assembler directives. |
| **`parser.py`** | Whitespace-tolerant assembly line tokenizer. |
| **`utils.py`** | Hexadecimal, integer, and BYTE literal conversions. |
| **`input.asm`** | The active batch-allotted assembly source program. |

---

## 💻 Batch-Allotted Program (`input.asm`)

```sic
COUNT   START   9000
        LDX     ZERO        ; Initialize X = 0 (Index Register)
        LDA     ZERO        ; Initialize Accumulator A = 0
        STA     COUNT1      ; COUNT1 = 0

LOOP    LDA     TABLE       ; Load element from TABLE
        COMP    ZERO        ; Compare element with 0
        JLT     NEXT        ; If element < 0, skip increment
        LDA     COUNT1      ; Load current count
        ADD     ONE         ; Increment: COUNT1 + 1
        STA     COUNT1      ; Store back to COUNT1

NEXT    TIX     FIVE        ; X = X + 1, Compare X with 5
        JLT     LOOP        ; If X < 5, repeat loop
        RSUB                ; Return from subroutine

TABLE   WORD    10          ; Array element 0: +10
        WORD    -5          ; Array element 1: -5 (Negative)
        WORD    20          ; Array element 2: +20
        WORD    -2          ; Array element 3: -2 (Negative)
        WORD    15          ; Array element 4: +15

COUNT1  RESW    1           ; Reserve 1 word for positive count
ZERO    WORD    0           ; Constant 0
ONE     WORD    1           ; Constant 1
FIVE    WORD    5           ; Loop boundary limit (5)
        END     COUNT       ; End of program, execution starts at COUNT
```

---

## 🚀 How to Run the Simulation

### 1. Terminal / Command-Line Simulation
```bash
python3 main.py
```

### 2. Desktop GUI Simulator (Tkinter)
```bash
python3 gui.py
```

### 3. Interactive Web Simulator
Open `index.html` in any web browser.

---

## 📊 Complete Simulation Results

### 1. Symbol Table (SYMTAB)
```text
SYMBOL              ADDRESS (HEX)
---------------------------------
LOOP                9009
NEXT                901B
TABLE               9024
COUNT1              9033
ZERO                9036
ONE                 9039
FIVE                903C
```
* **Starting Address:** `9000 H`
* **Program Length:** $903F_{16} - 9000_{16} = \mathbf{003F_{16}} = \mathbf{63 \text{ Bytes}}$

### 2. Object Code Listing
```text
ADDRESS     SOURCE STATEMENT                OBJECT CODE
---------------------------------------------------------
9000        COUNT   START   9000            --
9000        LDX     ZERO                    049036
9003        LDA     ZERO                    009036
9006        STA     COUNT1                  0C9033
9009        LOOP    LDA     TABLE           009024
900C        COMP    ZERO                    289036
900F        JLT     NEXT                    38901B
9012        LDA     COUNT1                  009033
9015        ADD     ONE                     189039
9018        STA     COUNT1                  0C9033
901B        NEXT    TIX     FIVE            2C903C
901E        JLT     LOOP                    389009
9021        RSUB                            4C0000
9024        TABLE   WORD    10              00000A
9027        WORD    -5                      FFFFFB
902A        WORD    20                      000014
902D        WORD    -2                      FFFFFE
9030        WORD    15                      00000F
9033        COUNT1  RESW    1               --
9036        ZERO    WORD    0               000000
9039        ONE     WORD    1               000001
903C        FIVE    WORD    5               000005
903F        END     COUNT                   --
```

### 3. Generated HTE Object Program
```text
H^COUNT ^009000^00003F
T^009000^1E^0490360090360C903300902428903638901B0090331890390C90332C903C
T^00901E^15^3890094C000000000AFFFFFB000014FFFFFE00000F
T^009036^09^000000000001000005
E^009000
```

---

## 🧮 Two's Complement Mathematics for Negative Constants

In standard SIC, a word is 24 bits ($3$ bytes). Negative values are represented as:

$$\text{2's Complement} = 2^{24} - |V| = 16,777,216 - |V|$$

* **`WORD -5`:** $16,777,216 - 5 = 16,777,211_{10} = \mathbf{FFFFFB_{16}}$
* **`WORD -2`:** $16,777,216 - 2 = 16,777,214_{10} = \mathbf{FFFFFE_{16}}$

---

## 📚 References

1. Beck, Leland L. *System Software: An Introduction to Systems Programming*. 3rd ed., Addison-Wesley, 1997. Chapter 2 (Assemblers).
2. Base repository: [DhruvaKumar18/SIC_Simulation](https://github.com/DhruvaKumar18/SIC_Simulation)
