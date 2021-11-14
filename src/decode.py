from dataclasses import dataclass
from numpy import uint32, int32
from enum import Enum


def sign_extend(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)


@dataclass
class Decoder:
    """Separates instruction into respective fields.

    Args:
        _instruction (uint32): The instruction to decode."""

    _instruction: uint32

    @property
    def opcode(self):
        return extract_bits(self._instruction, 7, 0)

    @property
    def funct3(self):
        return extract_bits(self._instruction, 3, 12)

    @property
    def funct7(self):
        return extract_bits(self._instruction, 7, 25)

    @property
    def rd(self):
        return extract_bits(self._instruction, 5, 7)

    @property
    def rs1(self):
        return extract_bits(self._instruction, 5, 15)

    @property
    def rs2(self):
        return extract_bits(self._instruction, 5, 20)

    @property
    def shamt(self):
        return extract_bits(self._instruction, 5, 20)

    @property
    def imm_i(self):
        return sign_extend(extract_bits(self._instruction, 12, 20), 12)

    @property
    def imm_u(self):
        return int32(extract_bits(self._instruction, 20, 12) << 12)

    @property
    def imm_s(self):
        b_4_0 = extract_bits(self._instruction, 6, 7)
        b_11_5 = extract_bits(self._instruction, 7, 25)
        return concatenate_binary_strings(b_11_5, b_4_0)

    @property
    def imm_b(self):
        b_4_1 = extract_bits(self._instruction, 4, 8)
        b_10_5 = extract_bits(self._instruction, 6, 25)
        b_11 = extract_bits(self._instruction, 1, 7)
        b_12 = extract_bits(self._instruction, 1, 31)
        return sign_extend((((b_12 << 1 | b_11) << 6 | b_10_5) << 4 | b_4_1), 12) << 1

    @property
    def imm_j(self):
        b_10_1 = extract_bits(self._instruction, 10, 21)
        b_11 = extract_bits(self._instruction, 1, 20)
        b_19_12 = extract_bits(self._instruction, 8, 12)
        b_20 = extract_bits(self._instruction, 1, 31)
        return concatenate_binary_strings(b_20, b_19_12, b_11, b_10_1)


# Helper Functions
def extract_bits(number: uint32, num_bits: int, start_position: int) -> uint32:
    """Extracts specified bits from and integer.

    Args:
        no (uint32): The number from which to extract bits
        num_bits (int): The number of bits to extract
        start_position (int): The start position from which to extract the bits.
            0 indexed and references the least significant bit.

    Returns:
        uint32: The resulting extracted bits

    """

    return (number >> start_position) & (2 ** num_bits - 1)


def concatenate_binary_strings(*args: uint32) -> uint32:
    """Returns the resulting integer from concatenating binary digits.

    Args:
        *args (uint32): A series of integers to be concatenated in their binary
            representation

    Returns:
        uint32: The resulting integer from concatenating all binary
            representations of the provided integers

    """

    binary_strings = [bin(arg)[2:] for arg in args]
    binary_strings.insert(0, "0b")
    return uint32(int("".join(binary_strings), 2))


# Match patterns
class Opcode(Enum):
    """Binding of instrcution names/classifications to their respective opcode."""

    LUI = 0b0110111
    AUIPC = 0b0010111
    JAL = 0b1101111
    JALR = 0b1100111

    B_TYPE = 0b1100011
    I_TYPE_LOAD = 0b0000011
    S_TYPE = 0b0100011
    I_TYPE = 0b0010011
    R_TYPE = 0b0110011

    ECALL = 0b1110011


class Funct3(Enum):
    """Binding of instructions to their respective funct3 value."""

    BEQ = 0b000
    BNE = 0b001
    BLT = 0b100
    BGE = 0b101
    BLTU = 0b110
    BGEU = 0b111

    LB = 0b000
    LH = 0b001
    LW = 0b010
    LBU = 0b100
    LHU = 0b101

    SB = 0b000
    SH = 0b001
    SW = 0b010

    ADDI = 0b000
    SLTI = 0b010
    SLTIU = 0b011
    XORI = 0b100
    ORI = 0b110
    ANDI = 0b111
    SLLI = 0b001
    SRLI_SRAI = 0b101

    ADD_SUB = 0b000
    SLL = 0b001
    SLT = 0b010
    SLTU = 0b011
    XOR = 0b100
    SRL_SRA = 0b101
    OR = 0b110
    AND = 0b111


class Funct7(Enum):
    """Binding of instructions to their respective funct7 value."""

    SRLI = 0b0000000
    SRAI = 0b0100000

    ADD = 0b0000000
    SUB = 0b0100000

    SRL = 0b0000000
    SRA = 0b0100000
