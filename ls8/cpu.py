"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = False

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # MAR = memory address register <-- address being read
    def ram_read(self, MAR):
        MDR = self.ram[MAR]
        return MDR

    # MAR <-- address being written tO; MDR = memory data register <-- data being written to address
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""
        # Define instruction values per specs
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111

        # set running to True
        self.running = True

        # Iterate thru
        while self.running:
            # set instruction register
            ir = self.ram_read(self.pc)

            # HLT INSTRUCTION: Halt CPU & exit emulator
            if ir is HLT:
                self.running = False

            # LDI INSTRUCTION: Set value of register to an integer
            elif ir is LDI:
                # define register number
                operand_a = self.ram_read(self.pc+1)
                # define 8-bit immediate value
                operand_b = self.ram_read(self.pc+2)
                # update register
                self.reg[operand_a] = operand_b
                # increment pc
                self.pc += 3

            # PRN INSTRUCTION: print numeric value stored in given register
            elif ir is PRN:
                # define register number
                operand_a = self.ram_read(self.pc+1)
                # print the value
                print(f"Value at {operand_a}: {self.reg[operand_a]}")
                # increment pc
                self.pc += 2
