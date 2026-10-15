# ============================================================
# TWO-PASS SIC ASSEMBLER - GUI SIMULATOR
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox

from opcode_table import OPTAB
from parser import parse_line
from utils import (
    hex_to_int,
    int_to_hex,
    byte_length,
    generate_byte_object_code
)


class TwoPassAssemblerGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Two-Pass SIC Assembler Simulator"
        )

        self.root.geometry("1250x750")

        self.root.minsize(1000, 650)

        # ----------------------------------------------------
        # VARIABLES
        # ----------------------------------------------------

        self.source_lines = []

        self.parsed_lines = []

        self.symbol_table = {}

        self.intermediate = []

        self.object_codes = []

        self.start_address = None

        self.program_length = 0

        self.locctr = None

        self.pass1_index = 0

        self.pass2_index = 0

        self.pass1_finished = False

        self.pass2_finished = False

        # ----------------------------------------------------
        # CREATE GUI
        # ----------------------------------------------------

        self.create_header()

        self.create_control_panel()

        self.create_source_panel()

        self.create_tables()

        self.create_status_bar()

        # ----------------------------------------------------
        # LOAD PROGRAM
        # ----------------------------------------------------

        self.load_program()


    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg="#1f2937",
            height=70
        )

        header.pack(
            fill="x"
        )

        title = tk.Label(
            header,
            text="TWO-PASS SIC ASSEMBLER",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#1f2937"
        )

        title.pack(
            pady=(10, 2)
        )

        subtitle = tk.Label(
            header,
            text="Interactive Assembler Simulation",
            font=("Arial", 11),
            fg="#d1d5db",
            bg="#1f2937"
        )

        subtitle.pack()


    # ========================================================
    # CONTROL PANEL
    # ========================================================

    def create_control_panel(self):

        panel = tk.Frame(
            self.root,
            padx=10,
            pady=10
        )

        panel.pack(
            fill="x"
        )

        # Start Pass 1
        self.start_pass1_button = tk.Button(
            panel,
            text="Start Pass 1",
            width=15,
            command=self.start_pass1,
            bg="#2563eb",
            fg="white",
            font=("Arial", 10, "bold")
        )

        self.start_pass1_button.pack(
            side="left",
            padx=5
        )

        # Next Pass 1
        self.next_pass1_button = tk.Button(
            panel,
            text="Next Pass 1",
            width=15,
            command=self.next_pass1,
            state="disabled",
            bg="#059669",
            fg="white",
            font=("Arial", 10, "bold")
        )

        self.next_pass1_button.pack(
            side="left",
            padx=5
        )

        # Start Pass 2
        self.start_pass2_button = tk.Button(
            panel,
            text="Start Pass 2",
            width=15,
            command=self.start_pass2,
            state="disabled",
            bg="#7c3aed",
            fg="white",
            font=("Arial", 10, "bold")
        )

        self.start_pass2_button.pack(
            side="left",
            padx=5
        )

        # Next Pass 2
        self.next_pass2_button = tk.Button(
            panel,
            text="Next Pass 2",
            width=15,
            command=self.next_pass2,
            state="disabled",
            bg="#dc2626",
            fg="white",
            font=("Arial", 10, "bold")
        )

        self.next_pass2_button.pack(
            side="left",
            padx=5
        )

        # Reset
        self.reset_button = tk.Button(
            panel,
            text="Reset",
            width=15,
            command=self.reset,
            bg="#374151",
            fg="white",
            font=("Arial", 10, "bold")
        )

        self.reset_button.pack(
            side="left",
            padx=5
        )


    # ========================================================
    # SOURCE PROGRAM
    # ========================================================

    def create_source_panel(self):

        frame = tk.LabelFrame(
            self.root,
            text="Source Program",
            font=("Arial", 11, "bold"),
            padx=5,
            pady=5
        )

        frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.source_text = tk.Text(
            frame,
            height=9,
            font=("Consolas", 11),
            bg="#111827",
            fg="#f9fafb"
        )

        self.source_text.pack(
            fill="x"
        )


    # ========================================================
    # TABLES
    # ========================================================

    def create_tables(self):

        container = tk.Frame(
            self.root
        )

        container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        # ----------------------------------------------------
        # SYMBOL TABLE
        # ----------------------------------------------------

        symbol_frame = tk.LabelFrame(
            container,
            text="Symbol Table",
            font=("Arial", 11, "bold")
        )

        symbol_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 5)
        )

        self.symbol_tree = ttk.Treeview(
            symbol_frame,
            columns=("symbol", "address"),
            show="headings",
            height=12
        )

        self.symbol_tree.heading(
            "symbol",
            text="Symbol"
        )

        self.symbol_tree.heading(
            "address",
            text="Address"
        )

        self.symbol_tree.column(
            "symbol",
            width=130
        )

        self.symbol_tree.column(
            "address",
            width=100
        )

        self.symbol_tree.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # INTERMEDIATE CODE
        # ----------------------------------------------------

        intermediate_frame = tk.LabelFrame(
            container,
            text="Intermediate Code",
            font=("Arial", 11, "bold")
        )

        intermediate_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        self.intermediate_tree = ttk.Treeview(
            intermediate_frame,
            columns=(
                "address",
                "label",
                "opcode",
                "operand"
            ),
            show="headings",
            height=12
        )

        self.intermediate_tree.heading(
            "address",
            text="Address"
        )

        self.intermediate_tree.heading(
            "label",
            text="Label"
        )

        self.intermediate_tree.heading(
            "opcode",
            text="Opcode"
        )

        self.intermediate_tree.heading(
            "operand",
            text="Operand"
        )

        self.intermediate_tree.column(
            "address",
            width=80
        )

        self.intermediate_tree.column(
            "label",
            width=90
        )

        self.intermediate_tree.column(
            "opcode",
            width=80
        )

        self.intermediate_tree.column(
            "operand",
            width=130
        )

        self.intermediate_tree.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # OBJECT CODE
        # ----------------------------------------------------

        object_frame = tk.LabelFrame(
            container,
            text="Object Code",
            font=("Arial", 11, "bold")
        )

        object_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(5, 0)
        )

        self.object_tree = ttk.Treeview(
            object_frame,
            columns=(
                "address",
                "source",
                "object"
            ),
            show="headings",
            height=12
        )

        self.object_tree.heading(
            "address",
            text="Address"
        )

        self.object_tree.heading(
            "source",
            text="Source"
        )

        self.object_tree.heading(
            "object",
            text="Object Code"
        )

        self.object_tree.column(
            "address",
            width=80
        )

        self.object_tree.column(
            "source",
            width=150
        )

        self.object_tree.column(
            "object",
            width=120
        )

        self.object_tree.pack(
            fill="both",
            expand=True
        )


    # ========================================================
    # STATUS BAR
    # ========================================================

    def create_status_bar(self):

        status_frame = tk.Frame(
            self.root,
            padx=10,
            pady=5
        )

        status_frame.pack(
            fill="x"
        )

        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            anchor="w",
            font=("Arial", 11, "bold")
        )

        self.status_label.pack(
            side="left"
        )

        self.locctr_label = tk.Label(
            status_frame,
            text="LOCCTR: --",
            anchor="e",
            font=("Consolas", 11, "bold")
        )

        self.locctr_label.pack(
            side="right"
        )


    # ========================================================
    # LOAD INPUT PROGRAM
    # ========================================================

    def load_program(self):

        try:

            with open(
                "input.asm",
                "r",
                encoding="utf-8"
            ) as file:

                self.source_lines = file.readlines()

        except FileNotFoundError:

            messagebox.showerror(
                "Error",
                "input.asm not found."
            )

            return

        self.source_text.delete(
            "1.0",
            tk.END
        )

        for line in self.source_lines:

            self.source_text.insert(
                tk.END,
                line
            )

        self.prepare_parsed_lines()


    # ========================================================
    # PARSE SOURCE
    # ========================================================

    def prepare_parsed_lines(self):

        self.parsed_lines = []

        for line in self.source_lines:

            label, opcode, operand = parse_line(
                line
            )

            if opcode is None:
                continue

            self.parsed_lines.append({
                "label": label,
                "opcode": opcode,
                "operand": operand,
                "source": line.strip()
            })


    # ========================================================
    # START PASS 1
    # ========================================================

    def start_pass1(self):

        self.symbol_table = {}

        self.intermediate = []

        self.pass1_index = 0

        self.pass1_finished = False

        self.locctr = None

        self.start_address = None

        self.program_length = 0

        # Clear tables
        self.clear_tree(
            self.symbol_tree
        )

        self.clear_tree(
            self.intermediate_tree
        )

        self.clear_tree(
            self.object_tree
        )

        self.start_pass1_button.config(
            state="disabled"
        )

        self.next_pass1_button.config(
            state="normal"
        )

        self.start_pass2_button.config(
            state="disabled"
        )

        self.next_pass2_button.config(
            state="disabled"
        )

        self.status_label.config(
            text="PASS 1 started — click Next Pass 1"
        )

        self.locctr_label.config(
            text="LOCCTR: --"
        )


    # ========================================================
    # NEXT PASS 1 STEP
    # ========================================================

    def next_pass1(self):

        if self.pass1_index >= len(
            self.parsed_lines
        ):

            self.finish_pass1()

            return

        entry = self.parsed_lines[
            self.pass1_index
        ]

        label = entry["label"]

        opcode = entry["opcode"]

        operand = entry["operand"]

        source = entry["source"]

        # ====================================================
        # START
        # ====================================================

        if opcode == "START":

            self.start_address = (
                hex_to_int(operand)
            )

            self.locctr = self.start_address

            self.intermediate.append({
                "address": self.locctr,
                "label": label or "",
                "opcode": opcode,
                "operand": operand or "",
                "source": source
            })

            self.add_intermediate_row(
                self.locctr,
                label,
                opcode,
                operand
            )

            self.update_locctr()

            self.pass1_index += 1

            self.status_label.config(
                text=f"PASS 1: START → {operand}"
            )

            return

        # ====================================================
        # END
        # ====================================================

        if opcode == "END":

            self.intermediate.append({
                "address": self.locctr,
                "label": label or "",
                "opcode": opcode,
                "operand": operand or "",
                "source": source
            })

            self.add_intermediate_row(
                self.locctr,
                label,
                opcode,
                operand
            )

            self.pass1_index += 1

            self.finish_pass1()

            return

        # ====================================================
        # CURRENT ADDRESS
        # ====================================================

        current_address = self.locctr

        # ====================================================
        # SYMBOL
        # ====================================================

        if label:

            if label in self.symbol_table:

                messagebox.showerror(
                    "Assembler Error",
                    f"Duplicate symbol: {label}"
                )

                return

            self.symbol_table[label] = (
                self.locctr
            )

            self.add_symbol_row(
                label,
                self.locctr
            )

        # ====================================================
        # INSTRUCTION
        # ====================================================

        if opcode in OPTAB:

            self.locctr += 3

        # ====================================================
        # WORD
        # ====================================================

        elif opcode == "WORD":

            self.locctr += 3

        # ====================================================
        # BYTE
        # ====================================================

        elif opcode == "BYTE":

            self.locctr += byte_length(
                operand
            )

        # ====================================================
        # RESW
        # ====================================================

        elif opcode == "RESW":

            self.locctr += (
                3 * int(operand)
            )

        # ====================================================
        # RESB
        # ====================================================

        elif opcode == "RESB":

            self.locctr += int(operand)

        else:

            messagebox.showerror(
                "Assembler Error",
                f"Unknown opcode: {opcode}"
            )

            return

        # ====================================================
        # ADD INTERMEDIATE CODE
        # ====================================================

        self.intermediate.append({
            "address": current_address,
            "label": label or "",
            "opcode": opcode,
            "operand": operand or "",
            "source": source
        })

        self.add_intermediate_row(
            current_address,
            label,
            opcode,
            operand
        )

        self.pass1_index += 1

        self.update_locctr()

        self.status_label.config(
            text=(
                f"PASS 1: Processing "
                f"{source}"
            )
        )


    # ========================================================
    # FINISH PASS 1
    # ========================================================

    def finish_pass1(self):

        if self.locctr is not None:

            self.program_length = (
                self.locctr -
                self.start_address
            )

        self.pass1_finished = True

        self.next_pass1_button.config(
            state="disabled"
        )

        self.start_pass2_button.config(
            state="normal"
        )

        self.status_label.config(
            text=(
                "PASS 1 completed — "
                "Symbol Table generated"
            )
        )

        self.update_locctr()

        messagebox.showinfo(
            "Pass 1 Complete",
            (
                "PASS 1 completed successfully.\n\n"
                f"Program length: "
                f"{int_to_hex(self.program_length)} "
                f"hex"
            )
        )


    # ========================================================
    # START PASS 2
    # ========================================================

    def start_pass2(self):

        self.pass2_index = 0

        self.object_codes = []

        self.pass2_finished = False

        self.clear_tree(
            self.object_tree
        )

        self.start_pass2_button.config(
            state="disabled"
        )

        self.next_pass2_button.config(
            state="normal"
        )

        self.status_label.config(
            text="PASS 2 started — click Next Pass 2"
        )


    # ========================================================
    # NEXT PASS 2
    # ========================================================

    def next_pass2(self):

        if self.pass2_index >= len(
            self.intermediate
        ):

            self.finish_pass2()

            return

        entry = self.intermediate[
            self.pass2_index
        ]

        address = entry["address"]

        opcode = entry["opcode"]

        operand = entry["operand"]

        source = entry["source"]

        object_code = ""

        # ====================================================
        # MACHINE INSTRUCTION
        # ====================================================

        if opcode in OPTAB:

            machine_opcode = OPTAB[
                opcode
            ]

            # -----------------------------------------------
            # RSUB
            # -----------------------------------------------

            if opcode == "RSUB":

                object_code = (
                    machine_opcode +
                    "0000"
                )

            else:

                indexed = False
                clean_op = operand
                if operand.endswith(",X") or ", X" in operand:
                    indexed = True
                    clean_op = operand.replace(", X", "").replace(",X", "").strip()

                if clean_op not in self.symbol_table:

                    messagebox.showerror(
                        "Assembler Error",
                        (
                            f"Undefined symbol: "
                            f"{operand}"
                        )
                    )

                    return

                operand_address = (
                    self.symbol_table[
                        clean_op
                    ]
                )

                if indexed:
                    operand_address += 0x8000

                object_code = (
                    machine_opcode +
                    int_to_hex(
                        operand_address,
                        4
                    )
                )

        # ====================================================
        # WORD
        # ====================================================

        elif opcode == "WORD":

            value = int(operand)

            object_code = format(
                value & 0xFFFFFF,
                "06X"
            )

        # ====================================================
        # BYTE
        # ====================================================

        elif opcode == "BYTE":

            object_code = (
                generate_byte_object_code(
                    operand
                )
            )

        # ====================================================
        # RESERVED
        # ====================================================

        elif opcode in (
            "RESW",
            "RESB"
        ):

            object_code = ""

        # ====================================================
        # START / END
        # ====================================================

        elif opcode in (
            "START",
            "END"
        ):

            object_code = ""

        # ====================================================
        # STORE RESULT
        # ====================================================

        self.object_codes.append({
            "address": address,
            "source": source,
            "object_code": object_code
        })

        self.add_object_row(
            address,
            source,
            object_code
        )

        self.pass2_index += 1

        if object_code:

            self.status_label.config(
                text=(
                    f"PASS 2: {source} "
                    f"→ {object_code}"
                )
            )

        else:

            self.status_label.config(
                text=f"PASS 2: {source} → No object code"
            )


    # ========================================================
    # FINISH PASS 2
    # ========================================================

    def finish_pass2(self):

        self.pass2_finished = True

        self.next_pass2_button.config(
            state="disabled"
        )

        self.status_label.config(
            text=(
                "PASS 2 completed — "
                "Object Code generated"
            )
        )

        messagebox.showinfo(
            "Assembly Complete",
            (
                "Two-pass assembly completed "
                "successfully!"
            )
        )


    # ========================================================
    # SYMBOL TABLE ROW
    # ========================================================

    def add_symbol_row(
        self,
        symbol,
        address
    ):

        self.symbol_tree.insert(
            "",
            "end",
            values=(
                symbol,
                int_to_hex(address)
            )
        )


    # ========================================================
    # INTERMEDIATE CODE ROW
    # ========================================================

    def add_intermediate_row(
        self,
        address,
        label,
        opcode,
        operand
    ):

        self.intermediate_tree.insert(
            "",
            "end",
            values=(
                int_to_hex(address),
                label or "",
                opcode,
                operand or ""
            )
        )


    # ========================================================
    # OBJECT CODE ROW
    # ========================================================

    def add_object_row(
        self,
        address,
        source,
        object_code
    ):

        if not object_code:

            display_code = "--"

        else:

            display_code = object_code

        self.object_tree.insert(
            "",
            "end",
            values=(
                int_to_hex(address),
                source,
                display_code
            )
        )


    # ========================================================
    # LOCCTR UPDATE
    # ========================================================

    def update_locctr(self):

        if self.locctr is None:

            self.locctr_label.config(
                text="LOCCTR: --"
            )

        else:

            self.locctr_label.config(
                text=(
                    "LOCCTR: " +
                    int_to_hex(
                        self.locctr
                    )
                )
            )


    # ========================================================
    # CLEAR TREE
    # ========================================================

    def clear_tree(self, tree):

        for item in tree.get_children():

            tree.delete(item)


    # ========================================================
    # RESET
    # ========================================================

    def reset(self):

        self.symbol_table = {}

        self.intermediate = []

        self.object_codes = []

        self.pass1_index = 0

        self.pass2_index = 0

        self.pass1_finished = False

        self.pass2_finished = False

        self.start_address = None

        self.locctr = None

        self.program_length = 0

        self.clear_tree(
            self.symbol_tree
        )

        self.clear_tree(
            self.intermediate_tree
        )

        self.clear_tree(
            self.object_tree
        )

        self.start_pass1_button.config(
            state="normal"
        )

        self.next_pass1_button.config(
            state="disabled"
        )

        self.start_pass2_button.config(
            state="disabled"
        )

        self.next_pass2_button.config(
            state="disabled"
        )

        self.status_label.config(
            text="Ready — click Start Pass 1"
        )

        self.update_locctr()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = TwoPassAssemblerGUI(
        root
    )

    root.mainloop()