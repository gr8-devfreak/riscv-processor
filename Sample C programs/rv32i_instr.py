def register_to_number(reg):
    reg_map = {
        "zero": 0, "ra": 1, "sp": 2, "gp": 3, "tp": 4, "t0": 5,
        "t1": 6, "t2": 7, "s0": 8, "s1": 9, "a0": 10, "a1": 11,
        "a2": 12, "a3": 13, "a4": 14, "a5": 15, "a6": 16, "a7": 17,
        "s2": 18, "s3": 19, "s4": 20, "s5": 21, "s6": 22, "s7": 23,
        "s8": 24, "s9": 25, "s10": 26, "s11": 27, "t3": 28, "t4": 29,
        "t5": 30, "t6": 31
    }
    return reg_map.get(reg)

def parse_instruction(inst):
    parts = inst.split()
    opcode = parts[0]
    if opcode in ["add", "sub", "sll", "slt", "sltu", "xor", "srl", "sra", "or", "and"]:
        return "R", opcode, parts[1], parts[2], parts[3]
    elif opcode in ["addi", "slti", "sltiu", "xori", "ori", "andi", "slli", "srli", "srai"]:
        return "I", opcode, parts[1], parts[2], parts[3]
    else:
        return None

def assemble_r_type(opcode, rd, rs1, rs2):
    opcode_map = {
        "add": ("0110011", "0000000", "000"),
        "sub": ("0110011", "0100000", "000"),
        "sll": ("0110011", "0000000", "001"),
        "slt": ("0110011", "0000000", "010"),
        "sltu": ("0110011", "0000000", "011"),
        "xor": ("0110011", "0000000", "100"),
        "srl": ("0110011", "0000000", "101"),
        "sra": ("0110011", "0100000", "101"),
        "or": ("0110011", "0000000", "110"),
        "and": ("0110011", "0000000", "111"),
    }
    
    opcode_bits, funct7, funct3 = opcode_map[opcode]
    rd_bits = f"{register_to_number(rd):05b}"
    rs1_bits = f"{register_to_number(rs1):05b}"
    rs2_bits = f"{register_to_number(rs2):05b}"
    
    binary_instruction = funct7 + rs2_bits + rs1_bits + funct3 + rd_bits + opcode_bits
    hex_instruction = f"{int(binary_instruction, 2):08x}"
    
    return hex_instruction

def assemble_i_type(opcode, rd, rs1, imm):
    opcode_map = {
        "addi": ("0010011", "000"),
        "slti": ("0010011", "010"),
        "sltiu": ("0010011", "011"),
        "xori": ("0010011", "100"),
        "ori": ("0010011", "110"),
        "andi": ("0010011", "111"),
        "slli": ("0010011", "001"),
        "srli": ("0010011", "101"),
        "srai": ("0010011", "101"),
    }
    
    opcode_bits, funct3 = opcode_map[opcode]
    rd_bits = f"{register_to_number(rd):05b}"
    rs1_bits = f"{register_to_number(rs1):05b}"
    
    imm_value = int(imm)
    if imm_value < 0:
        imm_bits = f"{(1 << 12) + imm_value:012b}"
    else:
        imm_bits = f"{imm_value:012b}"
    
    if opcode == "srai":
        imm_bits = "0100000" + imm_bits[7:]  # For SRAI, the upper 7 bits of imm are funct7
    
    binary_instruction = imm_bits + rs1_bits + funct3 + rd_bits + opcode_bits
    hex_instruction = f"{int(binary_instruction, 2):08x}"
    
    return hex_instruction

def rv32i_to_hex(instruction):
    parsed = parse_instruction(instruction)
    if not parsed:
        return None
    
    inst_type, opcode, rd, rs1, rs2_or_imm = parsed
    
    if inst_type == "R":
        return assemble_r_type(opcode, rd, rs1, rs2_or_imm)
    elif inst_type == "I":
        return assemble_i_type(opcode, rd, rs1, rs2_or_imm)
    else:
        return None

# Example usage:
print(rv32i_to_hex("add t2, t3, t4"))  # Example R-type
print(rv32i_to_hex("addi t2, t3, 5"))  # Example I-type
