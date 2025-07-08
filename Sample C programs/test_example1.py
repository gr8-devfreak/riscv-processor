import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
from common import reset_dut, load_hex

@cocotb.test()
async def test_core_from_hexfile(dut):
    """ Test for example1.c """

    # Create a clock signal
    cocotb.start_soon(Clock(dut.i_clk, 10, units="ns").start())

    # Load hex file
    load_hex(dut=dut)

    # Reset the DUT
    await reset_dut(dut=dut)

    for _ in range(1000):
        await RisingEdge(dut.i_clk)

    print(f'Value at memory location 512 = {dut.inst_mem.memory_reg[512].value.integer}')
    print(f'Value at memory location 513 = {dut.inst_mem.memory_reg[513].value.integer}')
    print(f'Value at memory location 514 = {dut.inst_mem.memory_reg[514].value.integer}')
    print(f'Value at memory location 515 = {dut.inst_mem.memory_reg[515].value.integer}')
    print(f'Value at memory location 516 = {dut.inst_mem.memory_reg[516].value.integer}')
    print(f'Value at memory location 517 = {dut.inst_mem.memory_reg[517].value.integer}')
    print(f'Value at memory location 518 = {dut.inst_mem.memory_reg[518].value.integer}')

    assert dut.inst_mem.memory_reg[512].value.integer==100
    assert dut.inst_mem.memory_reg[513].value.integer==200
    assert dut.inst_mem.memory_reg[514].value.integer==300
    assert dut.inst_mem.memory_reg[515].value.integer==400
    assert dut.inst_mem.memory_reg[516].value.integer==1000
    assert dut.inst_mem.memory_reg[517].value.integer==2
    assert dut.inst_mem.memory_reg[518].value.integer==9


