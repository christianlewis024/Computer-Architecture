"""CPU functionality."""

import sys
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
# need to implement three instructions:
#
# LDI - load immediate, store a value in a register, or set this register to this value --- LDI  10000010 00000rrr iiiiiiii
#  PRN -a pseudo instruction that prints the numeric value stored in a register --- PRN  01000111 00000rrr
#  HLT - halt the cpu and exit the emulator HLT --- 00000001
# CMP  10100111 00000aaa 00000bbb
#  cmp - "cmp registerA registerB", compare the values in 2 registers
#       if they are equal set the equal 'e' flag to 1, otherwise set it to 0
#           if regA is less than regB, set the less-than 'L' flag to 1,
#               otherwise set it to 09
#
#


class CPU:

    """Main CPU class."""

    def __init__(self):
        self.branchtable = {}
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[JMP] = self.handle_JMP
        self.branchtable[JEQ] = self.handle_JEQ
        self.branchtable[JNE] = self.handle_JNE
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        # set the starting flag to 0
        self.flag = 0
        # # Program Counter, index into memory of the current instruction
        # AKA a pointer to the current instruction
        self.running = True
    # construct

    def handle_MUL(self, operand_a, operand_b):
        self.reg[operand_a] = self.reg[operand_a] * self.reg[operand_b]
        self.pc += 3

    def handle_HLT(self, operand_a, operand_b):
        sys.exit(1)

    def handle_PRN(self, operand_a, operand_b):
        print(self.reg[operand_a])
        self.pc += 2

    def handle_LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3

    def handle_CMP(self, operand_a, operand_b):
        # cmp - "cmp registerA registerB", compare the values in 2 registers
        #       if they are equal set the equal 'e' flag to 1, otherwise set it to 0
        #           if regA is less than regB, set the less-than 'L' flag to 1,
        #               otherwise set it to 09
        reg1 = self.ram[self.pc + 1]
        reg2 = self.ram[self.pc + 2]
        self.alu("CMP", reg1, reg2)
        self.pc += 3

    def handle_JMP(self, operand_a, operand_b):
        # Jump to the address stored in the given register.
        # Set the `PC` to the address stored in the given register.
        register = self.ram[self.pc + 1]
        self.pc = self.reg[register]

    def handle_JEQ(self, operand_a, operand_b):
        # If `equal` flag is set (true), jump to the address stored in the given register.
        register = self.ram[self.pc + 1]
        if (self.flag & HLT) > 0:
            self.pc = self.reg[register]
        else:
            self.pc += 2

    def handle_JNE(self, operand_a, operand_b):
        # If `E` flag is clear (false, 0), jump to the address stored in the given
        # register.
        register = self.ram[self.pc + 1]
        if (self.flag & HLT) == 0:
            self.pc = self.reg[register]
        else:
            self.pc += 2

    def ram_read(self, MAR):
        # Memory Address Register
        #  read and return the value of MAR
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        # Memory Data Register
        # accept value to write and the address to write it to
        self.ram[MAR] = MDR

    def load(self, newFile):
        #  load program into memory
        address = 0
        with open(newFile) as file:
            for line in file:
                val = line.split("#")[0].strip()
                if val == '':
                    continue
                instruction = int(val, 2)
                self.ram[address] = instruction
                address += 1
        """Load a program into memory."""

    #

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "CMP":
            # cmp - "cmp registerA registerB", compare the values in 2 registers
            #       if they are equal set the equal 'e' flag to 1, otherwise set it to 0
            #           if regA is less than regB, set the less-than 'L' flag to 1,
            #               otherwise set it to 09

            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001

            # elif self.reg[reg_a] > self.reg[reg_b]:
            #     self.flag = 0b00001001
            # elif self.reg[reg_a] < self.reg[reg_b]:
            #     self.flag = 0b00000001
            else:
                self.flag = 0b00000000
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

    def run(self):

        while self.running is True:
            self.trace()
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if IR in self.branchtable:
                self.branchtable[IR](operand_a, operand_b)
        """Run the CPU."""
        #  read the memory address stored in the register,
        #  run ram read on the register self.ram_read(self.pc)
        #  and store the results in the instruction register(IR) <- to be created in the run

        # Some instructions requires up to the next two bytes of data after the PC in memory to perform operations on.

        #  Sometimes the byte value is a register number, other times it's a constant value (in the case of LDI). Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them.
