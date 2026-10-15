# pass2.py

from opcode_table import OPTAB
from utils import (
    int_to_hex,
    generate_byte_object_code
)


def pass2(intermediate, symbol_table):

    print("\n")
    print("=" * 75)
    print("                         PASS 2")
    print("=" * 75)

    object_codes = []

    for entry in intermediate:

        address = entry["address"]

        opcode = entry["opcode"]

        operand = entry["operand"]

        object_code = ""

        # ==================================================
        # MACHINE INSTRUCTION
        # ==================================================

        if opcode in OPTAB:

            machine_opcode = OPTAB[opcode]

            # ----------------------------------------------
            # RSUB
            # ----------------------------------------------

            if opcode == "RSUB":

                object_code = (
                    machine_opcode +
                    "0000"
                )

            # ----------------------------------------------
            # Other instructions
            # ----------------------------------------------

            else:

                indexed = False
                clean_op = operand
                if operand.endswith(",X") or ", X" in operand:
                    indexed = True
                    clean_op = operand.replace(", X", "").replace(",X", "").strip()

                if clean_op not in symbol_table:

                    raise ValueError(
                        f"Undefined symbol: {operand}"
                    )

                operand_address = symbol_table[clean_op]

                if indexed:
                    operand_address += 0x8000

                object_code = (
                    machine_opcode +
                    int_to_hex(
                        operand_address,
                        4
                    )
                )

        # ==================================================
        # WORD
        # ==================================================

        elif opcode == "WORD":

            value = int(operand)

            # SIC uses 24-bit words; negative numbers use 2's complement
            object_code = format(
                value & 0xFFFFFF,
                "06X"
            )

        # ==================================================
        # BYTE
        # ==================================================

        elif opcode == "BYTE":

            object_code = (
                generate_byte_object_code(
                    operand
                )
            )

        # ==================================================
        # RESW / RESB
        # ==================================================

        elif opcode in ("RESW", "RESB"):

            object_code = ""

        # ==================================================
        # START / END
        # ==================================================

        elif opcode in ("START", "END"):

            object_code = ""

        # ==================================================
        # SAVE RESULT
        # ==================================================

        object_codes.append({
            "address": address,
            "source": entry["source"],
            "object_code": object_code
        })

        print(
            f"{int_to_hex(address):<10}"
            f"{entry['source']:<30}"
            f"{object_code}"
        )

    return object_codes


# ==========================================================
# DISPLAY OBJECT CODE
# ==========================================================

def display_object_code(object_codes):

    print("\n")
    print("=" * 75)
    print("                       OBJECT CODE")
    print("=" * 75)

    print(
        f"{'ADDRESS':<12}"
        f"{'SOURCE':<32}"
        f"{'OBJECT CODE':<20}"
    )

    print("-" * 65)

    for item in object_codes:

        object_code = item["object_code"]

        if object_code == "":

            object_code = "--"

        print(
            f"{int_to_hex(item['address']):<12}"
            f"{item['source']:<32}"
            f"{object_code:<20}"
        )


# ==========================================================
# GENERATE & DISPLAY OBJECT PROGRAM (HTE RECORDS)
# ==========================================================

def display_object_program(intermediate, object_codes, start_address, program_length):

    print("\n")
    print("=" * 75)
    print("               OBJECT PROGRAM (HTE RECORDS)")
    print("=" * 75)

    # 1. Program Name
    prog_name = "NONAME"
    first_entry = intermediate[0] if intermediate else None
    if first_entry and first_entry["opcode"] == "START" and first_entry["label"]:
        prog_name = first_entry["label"]

    prog_name_padded = f"{prog_name:<6}"[:6]

    # Header Record
    header_record = f"H^{prog_name_padded}^{int_to_hex(start_address, 6)}^{int_to_hex(program_length, 6)}"
    print(f"Header Record : {header_record}")
    print("-" * 75)

    # Text Records (Max 30 bytes / 0x1E per record, breaks on RESW/RESB)
    text_records = []
    current_t_start = None
    current_t_bytes = []
    current_t_len = 0  # in bytes

    for item in object_codes:
        code = item["object_code"]
        addr = item["address"]

        if not code:
            # End current text record if any on RESW/RESB/START/END
            if current_t_bytes:
                rec_len_hex = int_to_hex(current_t_len, 2)
                codes_str = "".join(current_t_bytes)
                text_records.append(f"T^{int_to_hex(current_t_start, 6)}^{rec_len_hex}^{codes_str}")
                current_t_start = None
                current_t_bytes = []
                current_t_len = 0
            continue

        byte_len = len(code) // 2

        # Check if adding this code exceeds max 30 bytes (0x1E) or if starting a new record
        if current_t_start is None:
            current_t_start = addr
            current_t_bytes = [code]
            current_t_len = byte_len
        elif current_t_len + byte_len > 30:
            rec_len_hex = int_to_hex(current_t_len, 2)
            codes_str = "".join(current_t_bytes)
            text_records.append(f"T^{int_to_hex(current_t_start, 6)}^{rec_len_hex}^{codes_str}")
            current_t_start = addr
            current_t_bytes = [code]
            current_t_len = byte_len
        else:
            current_t_bytes.append(code)
            current_t_len += byte_len

    if current_t_bytes:
        rec_len_hex = int_to_hex(current_t_len, 2)
        codes_str = "".join(current_t_bytes)
        text_records.append(f"T^{int_to_hex(current_t_start, 6)}^{rec_len_hex}^{codes_str}")

    print("Text Records  :")
    for tr in text_records:
        print(f"  {tr}")

    print("-" * 75)

    # End Record
    end_record = f"E^{int_to_hex(start_address, 6)}"
    print(f"End Record    : {end_record}")
   