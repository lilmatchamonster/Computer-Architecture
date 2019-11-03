"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        # 130, 0, 8, 71, 0, 1

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]
        here = []
        try:
            with open(program) as file:
                for line in file:
                    split_line = line.split('#')
                    command_line = split_line[0]
                    if len(command_line) > 0:
                        command_line.strip()
                    if command_line[0] == '1' or command_line[0] == '0':
                        here = command_line.strip()
                        self.ram[address] = int(here, 2)
                        address += 1
        except FileNotFoundError:
            print('File does not exist')

        # for instruction in program:
        #     self.ram[address] = instruction
        #     print(program)
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # Instruction Register
        running = True

        while running:

            ir = self.ram[self.pc]   
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

            if ir == LDI:
                print(f'LDI ir is: {ir}')
                self.reg[operand_a] = operand_b
                print(f'reg is now: {self.reg[operand_a]}')
                self.pc += 3

            elif ir == PRN:
                print(f'PRN ir is: {ir}')
                value = self.reg[operand_a]
                print(value)
                self.pc += 2

            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            elif ir == HLT:
                print(f'Entered HLT. CPU ending...')
                running = False

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
    