# Two-Pass SIC Assembler

A simple Python implementation of a two-pass SIC assembler that reads a SIC-style assembly program, assigns memory addresses, builds a symbol table, and generates object code.

## Overview

This project simulates the classic assembler flow:

1. Pass 1 scans the source code and assigns locations using LOCCTR.
2. It records labels in the symbol table and keeps an intermediate representation of the program.
3. Pass 2 resolves symbolic operands and produces machine/object code.
4. The program prints the symbol table, intermediate code, and assembled object code.

## Features

- Handles SIC instruction mnemonics and directives
- Supports labels and symbolic operands
- Calculates the start address and program length
- Generates object code for instructions, WORD, and BYTE constants
- Detects common assembly errors such as duplicate symbols, undefined labels, invalid BYTE operands, and missing START directives

## Supported Instructions

The assembler includes the following SIC-style instructions:

- Load and store: LDA, LDX, LDL, STA, STX, STL
- Arithmetic: ADD, SUB, MUL, DIV
- Comparison and branching: COMP, TIX, JEQ, JGT, JLT, J
- Subroutine: JSUB, RSUB
- I/O: TD, RD, WD

## Supported Directives

- START
- END
- WORD
- BYTE
- RESW
- RESB

## Project Structure

- `main.py` — entry point; runs Pass 1 and Pass 2
- `pass1.py` — calculates addresses, builds symbol table, and creates intermediate code
- `pass2.py` — converts intermediate code into machine/object code
- `opcode_table.py` — SIC opcode mapping
- `parser.py` — parses each assembly line into label, opcode, and operand
- `utils.py` — conversion and BYTE handling utilities
- `input.asm` — sample assembly input
- `Readme.md` — project documentation

## Example Input

The sample program in `input.asm` is:

```asm
DATA    START   5000

        LDA     NUM
        STA     RESULT
        RSUB

NUM     WORD    100
CHAR    BYTE    C'HELLO'
HEXVAL  BYTE    X'F1'
RESULT  RESW    1

        END     DATA
```

## Running the Assembler

From the project directory:

```bash
cd two_pass_assembler
python main.py
```

On Windows, you can also use:

```bash
py main.py
```

The program reads `input.asm` automatically and prints:

- the symbol table
- the intermediate code
- the program start address
- the program length
- the generated object code

## Notes

- The assembler assumes the source file is named `input.asm` in the same directory as `main.py`.
- `BYTE` values support both character constants like `C'HELLO'` and hexadecimal constants like `X'F1'`.
- The implementation is intended for learning and demonstration of the SIC two-pass assembly process.

## Typical Output Sections

When executed, the program prints:

- PASS 1 details
- SYMBOL TABLE
- INTERMEDIATE CODE
- PROGRAM INFORMATION
- PASS 2 details
- OBJECT CODE
- ASSEMBLY COMPLETED

This makes it useful for understanding how a real assembler assigns memory and resolves labels during code generation.

## Files work together
```structure
main.py
   │
   ├── reads input.asm
   │
   ↓
pass1.py
   │
   ├── parser.py
   │       └── separates label/opcode/operand
   │
   ├── opcode_table.py
   │       └── checks instructions
   │
   ├── utils.py
   │       └── address/byte calculations
   │
   └── produces:
          ├── SYMTAB
          └── Intermediate Code
                    │
                    ↓
                 pass2.py
                    │
                    ├── opcode_table.py
                    ├── SYMTAB
                    └── utils.py
                    │
                    ↓
                Object Code
```

## Working procedure

## Pass 1 algorithm works
```Pass 1 algorithm working procedure
START
  ↓
Read first line
  ↓
Initialize LOCCTR
  ↓
Read next line
  ↓
Is there a label?
  ├── YES → Add LABEL + LOCCTR to SYMTAB
  └── NO
  ↓
Is it an instruction?
  ├── YES → LOCCTR = LOCCTR + 3
  └── NO
  ↓
Is it WORD?
  ├── YES → LOCCTR = LOCCTR + 3
  ↓
Is it RESW?
  ├── YES → LOCCTR = LOCCTR + 3 × operand
  ↓
Is it RESB?
  ├── YES → LOCCTR = LOCCTR + operand
  ↓
Is it BYTE?
  ├── YES → calculate BYTE size
  ↓
Is it END?
  ├── YES → Stop
  └── NO → Read next line

## Pass 2 algorithm works

START
  ↓
Read intermediate file
  ↓
Read next line
  ↓
Is it START?
  ↓
Skip
  ↓
Is opcode in OPTAB?
  ├── YES
  │    ↓
  │  Get opcode
  │    ↓
  │  Find operand in SYMTAB
  │    ↓
  │  Generate object code
  │
  └── NO
       ↓
     Is WORD?
       ↓
     Generate 3-byte value

     Is BYTE?
       ↓
     Convert to hexadecimal

     Is RESW / RESB?
       ↓
     No object code
  ↓
Is END?
  ├── YES → Generate End Record
  └── NO → Read next line
  ↓
STOP
```
## TWO-PASS ASSEMBLER
```Pass2 algorithm working 
SOURCE PROGRAM
       │
       ▼
   ┌─────────┐
   │ PASS 1  │
   └─────────┘
       │
       ├── SYMTAB
       ├── LOCCTR
       ├── Addresses
       └── Intermediate File
              │
              ▼
        ┌─────────┐
        │ PASS 2  │
        └─────────┘
              │
              ├── OPTAB
              ├── SYMTAB
              └── Intermediate File
                     │
                     ▼
               OBJECT CODE
                     │
                     ▼
              OBJECT PROGRAM
```
