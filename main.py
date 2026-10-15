# main.py

from pass1 import (
    pass1,
    display_symbol_table,
    display_intermediate
)

from pass2 import (
    pass2,
    display_object_code,
    display_object_program
)


def main():

    print("=" * 75)
    print("                  TWO-PASS SIC ASSEMBLER")
    print("                         SIMULATOR")
    print("=" * 75)

    filename = "input.asm"

    # ======================================================
    # READ SOURCE PROGRAM
    # ======================================================

    try:

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            source_lines = file.readlines()

    except FileNotFoundError:

        print(
            f"\nERROR: {filename} not found."
        )

        print(
            "\nMake sure input.asm is in the same "
            "folder as main.py."
        )

        return

    try:

        # ==================================================
        # PASS 1
        # ==================================================

        (
            symbol_table,
            intermediate,
            start_address,
            program_length
        ) = pass1(source_lines)

        # ==================================================
        # SYMBOL TABLE
        # ==================================================

        display_symbol_table(
            symbol_table
        )

        # ==================================================
        # INTERMEDIATE CODE
        # ==================================================

        display_intermediate(
            intermediate
        )

        # ==================================================
        # PROGRAM INFORMATION
        # ==================================================

        print("\n")
        print("=" * 75)
        print("                    PROGRAM INFORMATION")
        print("=" * 75)

        print(
            f"Starting Address : "
            f"{start_address:04X}"
        )

        print(
            f"Program Length   : "
            f"{program_length:04X} hex"
        )

        print(
            f"Program Length   : "
            f"{program_length} bytes"
        )

        # ==================================================
        # PASS 2
        # ==================================================

        object_codes = pass2(
            intermediate,
            symbol_table
        )

        # ==================================================
        # OBJECT CODE
        # ==================================================

        display_object_code(
            object_codes
        )

        # ==================================================
        # OBJECT PROGRAM (HTE RECORDS)
        # ==================================================

        display_object_program(
            intermediate,
            object_codes,
            start_address,
            program_length
        )

        # ==================================================
        # COMPLETE
        # ==================================================

        print("\n")
        print("=" * 75)
        print("                 ASSEMBLY COMPLETED")
        print("=" * 75)

    except ValueError as error:

        print("\n")
        print("=" * 75)
        print("                      ERROR")
        print("=" * 75)

        print(error)


if __name__ == "__main__":
    main()