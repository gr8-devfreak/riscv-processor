import cocotb
from cocotb.triggers import RisingEdge
from cocotb.clock import Clock
from cocotb.binary import BinaryValue
from common import reset_dut

@cocotb.test()
async def test_rv32i_instructions(dut):
    """ Test the complete RV32I instruction set of the RV32I CPU module """

    # Create a clock signal
    cocotb.start_soon(Clock(dut.i_clk, 10, units="ns").start())

    # Reset the DUT
    await reset_dut(dut)

    def assert_memory(actual, expected, addr):
        if actual.is_resolvable:
            if actual.integer != expected:
                print(f"     - Memory data mismatch M[] word address={addr} : expected {expected}, got {actual.integer}\n")
            assert actual.integer == expected
        else:
            print(f"     - Register data mismatch M[] word address={addr} : expected {expected}, got {actual}\n")
            assert False

    async def ignore_curr_instr():
        await RisingEdge(dut.i_clk)


    # Helper function to apply instruction and check result
    async def apply_instruction(instr, expected_result={}, expected_pc_increment=4, stall=False, name=""):
        dut.instruction_code.value = instr
        await RisingEdge(dut.i_clk)
        for k,v in expected_result.items():
            if dut.inst_ieu.inst_regfile.regs[k].value.is_resolvable:
                if dut.inst_ieu.inst_regfile.regs[k].value.integer != v:
                    print(f"     - Register data mismatch x{k}: expected {v}, got {dut.inst_ieu.inst_regfile.regs[k].value.integer}\n")
                assert dut.inst_ieu.inst_regfile.regs[k].value.integer == v
            else:
                print(f"     - Register data mismatch x{k}: expected {v}, got {dut.inst_ieu.inst_regfile.regs[k].value}\n")
                assert False
        
        print(f"Executing Instruction -- 0x{instr:08x} -- {name}")

        if dut.prev_pc.value.is_resolvable:
            if dut.prev_pc.value.integer != apply_instruction.pc:
                print(f"     - PC mismatch: expected {apply_instruction.pc}, got {dut.prev_pc.value.integer}\n")
                assert dut.prev_pc.value.integer == apply_instruction.pc
        else:
            print(f"     - PC mismatch: expected {apply_instruction.pc}, got {dut.prev_pc.value}\n")
            assert False

        if stall:
            await RisingEdge(dut.i_clk)

        apply_instruction.pc += expected_pc_increment

        
    apply_instruction.pc = 0

    print()
    ##########################################
    # BASIC SEQUENCE OF LOAD AND ARITHMENTIC #
    ##########################################

    r = {i:0 for i in range(32)}        # Registers

    # Load values into registers
    # LUI x1, 0x001  -> x1 = 0x00100000
    await apply_instruction(0x000010b7, expected_result=r, name="lui x1, 1")
    r[1] = (0x1)<<12

    # ADDI x1, x1, 0x004 -> x1 = 0x00100000 + 0x4 = 0x00100004
    await apply_instruction(0x00408093, expected_result=r, name="addi x1, x1, 4")
    r[1] = r[1]+0x4

    # LUI x2, 0x03  -> x2 = 0x00200000
    await apply_instruction(0x00003137, expected_result=r, name="lui x2, 3")
    r[2] = (0x3)<<12

    # ADDI x2, x2, 0x008 -> x2 = 0x00200000 + 0x8 = 0x00200008
    await apply_instruction(0x00810113, expected_result=r, name="addi x2, x2, 8")
    r[2] = r[2]+0x8

    # Perform arithmetic operations
    # ADD x3, x1, x2 -> x3 = 0x00100004 + 0x00200008 = 0x0030000C
    await apply_instruction(0x002081B3, expected_result=r, name="add x3, x1, x2")
    r[3] = r[1]+r[2]

    # SUB x4, x2, x1 -> x4 = 0x00200008 - 0x00100004 = 0x00100004
    await apply_instruction(0x40110233, expected_result=r, name="sub x4, x2, x1")
    r[4] = r[2]-r[1]

    # M not supoorted
    # MUL x5, x1, x2 -> x5 = 0x00100004 * 0x00200008 = 0x20000100 (assuming MUL is supported)
    # await apply_instruction(0x022082B3, expected_result=r)  # Replace with correct instruction for MUL if implemented
    # r[5] = r[1]*r[2]

    # print("Load and arithmetic operation tests completed successfully!")

    await apply_instruction(0x03250513, expected_result=r, name="addi x10, x10, 50")
    r[10] = 50

    await apply_instruction(0x1a758593, expected_result=r, name="addi x11, x11, 423")
    r[11] = 423

    await apply_instruction(0x00260613, expected_result=r, name="addi x12, x12, 2")
    r[12] = 2

    await apply_instruction(0xfffffbb7, expected_result=r, name="lui x23, -1")
    r[23] = BinaryValue('1'*20+'0'*12).integer

    await apply_instruction(0xf9cb8b93, expected_result=r, name="addi x23, x23, -100")
    r[23] = BinaryValue('1'*20+'111110011100').integer

    # R-type Instructions
    await apply_instruction(0x00B50533, expected_result=r, name="ADD x10, x10, x11")
    r[10] = r[10] + r[11]

    await apply_instruction(0x40B50533, expected_result=r, name="SUB x10, x10, x11")
    r[10] = r[10] - r[11]

    await apply_instruction(0x00c51533, expected_result=r, name="sll x10, x10, x12")
    r[10] = r[10] << r[12]

    await apply_instruction(0x00b526b3, expected_result=r, name="slt x13, x10, x11")
    r[13] = (r[10] < r[11])

    await apply_instruction(0x00b53733, expected_result=r, name="sltu x14, x10, x11")
    r[14] = (r[10] < r[11])

    await apply_instruction(0x00b547b3, expected_result=r, name="xor x15, x10, x11")
    r[15] = (r[10] ^ r[11])

    await apply_instruction(0x00d55533, expected_result=r, name="srl x10, x10, x13")
    r[10] = r[10] >> r[13]

    await apply_instruction(0x40e55533, expected_result=r, name="sra x10, x10, x14")
    r[10] = r[10] >> r[14]

    await apply_instruction(0x40ebdd33, expected_result=r, name="sra x26, x23, x14  // Signed test")
    tmp = BinaryValue(r[23]).binstr
    r[26] = BinaryValue(tmp[0]*r[14]+tmp[0:32-r[14]]).integer

    await apply_instruction(0x00b567b3, expected_result=r, name="or x15, x10, x11")
    r[15] = r[10] | r[11]

    await apply_instruction(0x00b57833, expected_result=r, name="and x16, x10, x11")
    r[16] = r[10] & r[11]

    # I-type Instructions
    await apply_instruction(0x00208113, expected_result=r, name="addi x0, x1, 2")
    r[2] = r[1] + 2

    await apply_instruction(0x06452113, expected_result=r, name="slti x2, x10, 100")
    r[2] = r[10] < 100

    await apply_instruction(0x02853893, expected_result=r, name="sltiu x17, x10, 40")
    r[17] = r[10] < 40

    await apply_instruction(0x0790c213, expected_result=r, name="xori x4, x1, 121")
    r[4] = r[1]^121

    await apply_instruction(0x07f0e293, expected_result=r, name="ori x5, x1, 127")
    r[5] = r[1]|127

    await apply_instruction(0x0021f093, expected_result=r, name="andi x1, x3, 2")
    r[1] = r[3]&2

    await apply_instruction(0x00221113, expected_result=r, name="slli x2, x4, 2")
    r[2] = r[4]<<2

    await apply_instruction(0x00225113, expected_result=r, name="srli x2, x4, 2")
    r[2] = r[4]>>2

    await apply_instruction(0x40225113, expected_result=r, name="srai x2, x4, 2")
    r[2] = r[4]>>2

    await apply_instruction(0x002bdc13, expected_result=r, name="srli x24, x23, 2   // Signed test")
    r[24] = r[23]>>2

    await apply_instruction(0x402bdc93, expected_result=r, name="srai x25, x23, 2   // Signed test")
    tmp = BinaryValue(r[23]).binstr
    r[25] = BinaryValue(tmp[0]*2+tmp[0:30]).integer
    prev_pc = apply_instruction.pc
    
    await apply_instruction(0x00a500e7, expected_result=r, name="jalr x1, 10(x10)")
    r[1]=prev_pc+4
    apply_instruction.pc = r[10]+10
    await ignore_curr_instr()

    # S-type Instructions
    await apply_instruction(0x7e700513, expected_result=r, name="addi x10, x0, 2023")
    r[10] = r[0] + 2023

    await apply_instruction(0x7e750513, expected_result=r, name="addi x10, x10, 2023")
    r[10] = r[10] + 2023

    await apply_instruction(0x7e750513, expected_result=r, name="addi x10, x10, 2023")
    r[10] = r[10] + 2023

    await apply_instruction(0x0c0f7537, expected_result=r, name="lui x10, 49399")
    r[10] = (49399<<12)

    await apply_instruction(0x7e750513, expected_result=r, name="addi x10, x10, 2023")
    r[10] = r[10] + 2023

    await apply_instruction(0x7e750513, expected_result=r, name="addi x10, x10, 2023")
    r[10] = r[10] + 2023


    await apply_instruction(0x00a708a3, r, 4, True, name="sb x10, 17(x14)")
    ad = r[14]+17
    assert_memory(dut.inst_mem.memory_reg[ad//4].value[32-(ad%4+1)*8:32-(ad%4)*8-1], r[10]&0xFF, ad//4)

    await apply_instruction(0x00a018a3, r, 4, True, name="sh x10, 17(x0)")
    ad = r[0]+17
    assert_memory(dut.inst_mem.memory_reg[ad//4].value[32-(((ad%4)//2)+1)*16:32-((ad%4)//2)*16-1], r[10]&0xFFFF, ad//4)

    await apply_instruction(0x00b009a3, r, 4, True, name="sb x11, 19(x0)")
    ad = r[0]+19
    assert_memory(dut.inst_mem.memory_reg[ad//4].value[32-(ad%4+1)*8:32-(ad%4)*8-1], r[11]&0xFF, ad//4)

    await apply_instruction(0x00a02b23, r, 4, True, name="sw x10, 22(x0)")
    ad = r[0]+22
    assert_memory(dut.inst_mem.memory_reg[ad//4].value, r[10], ad//4)

    
    await apply_instruction(0x01462083, r, 4, True, name="lw x1, 20(x12)")
    ad = r[12]+20
    r[1] = dut.inst_mem.memory_reg[ad//4].value

    await apply_instruction(0x01161103, r, 4, True, name="lh x2, 17(x12)         // Signed test")
    ad = r[12]+17
    v = dut.inst_mem.memory_reg[ad//4].value[32-(((ad%4)//2)+1)*16:32-((ad%4)//2)*16-1]
    r[2] = BinaryValue(v[0:0].binstr*16 + v.binstr)

    await apply_instruction(0x01600183, r, 4, True, name="lb x3, 22(x0)")
    ad = r[0]+22
    r[3] = dut.inst_mem.memory_reg[ad//4].value[32-(ad%4+1)*8:32-(ad%4)*8-1]

    await apply_instruction(0x01300283, r, 4, True, name="lb x5, 19(x0)          // Signed test")
    ad = r[0]+19
    v = dut.inst_mem.memory_reg[ad//4].value[32-(ad%4+1)*8:32-(ad%4)*8-1]
    r[5] = BinaryValue(v[0:0].binstr*24 + v.binstr)

    await apply_instruction(0x01165283, r, 4, True, name="lhu x5, 17(x12)")
    ad = r[12]+17
    v = dut.inst_mem.memory_reg[ad//4].value[32-(((ad%4)//2)+1)*16:32-((ad%4)//2)*16-1]
    r[5] = v

    await apply_instruction(0x01304283, r, 4, True, name="lbu x5, 19(x0)")
    ad = r[0]+19
    v = dut.inst_mem.memory_reg[ad//4].value[32-(ad%4+1)*8:32-(ad%4)*8-1]
    r[5] = v


    # B-type Instructions
    await apply_instruction(0x06000263, r, 100, name="beq x0, x0, 100")  # True
    await ignore_curr_instr()

    await apply_instruction(0x06100263, r, 4, name="beq x0, x1, 100")

    await apply_instruction(0x7c001863, r, 4, name="bne x0, x0, 2000")

    await apply_instruction(0x06314263, r, 100, name="blt x2, x3, 100   // Signed test")  # True
    await ignore_curr_instr()

    await apply_instruction(0x06225263, r, 100, name="bge x4, x2, 100   // Signed test")  # True
    await ignore_curr_instr()

    await apply_instruction(0x06316263, r, 4, name="bltu x2, x3, 100")  # False

    await apply_instruction(0x06317263, r, 100, name="bgeu x2, x3, 100")  # True
    await ignore_curr_instr()


    # U-type Instructions
    await apply_instruction(0x000020b7, r, 4, name="lui x1, 2")
    r[1] = 2<<12

    prev_pc = apply_instruction.pc
    await apply_instruction(0x00014217, r, 4, name="auipc x4, 20")
    r[4] = prev_pc + (20<<12)

    # J-type Instructions
    prev_pc = apply_instruction.pc
    await apply_instruction(0x000010EF, r, 2**12, name="JAL x1, 16")
    r[1] = (prev_pc)+4
    apply_instruction.pc = prev_pc + 2**12
    await ignore_curr_instr()

    await apply_instruction(0x000020b7, r, 4, name="lui x1, 2")
    r[1] = 2<<12

    await apply_instruction(0x000020b7, r, 4, name="lui x1, 2")
    r[1] = 2<<12
    

    print("All RV32I instruction tests completed successfully!")